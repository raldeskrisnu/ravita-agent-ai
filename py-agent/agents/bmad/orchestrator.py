"""BMad Orchestrator – LangGraph supervisor that routes tasks to specialised agents.

Architecture
------------
The orchestrator uses a LangGraph StateGraph with a supervisor node. The supervisor
LLM reads the conversation history and decides which BMad agent to invoke next, or
signals "FINISH" when the task is complete. Each agent node processes the current
message and appends its response to the shared state.

BMad Agents
-----------
- product_manager – requirements analysis, epics, stories, backlog, prioritisation, roadmap
- architect     – system design, ADRs, technical decisions
- developer     – code implementation, bug fixes (Ravita with full toolset)
- qa            – testing strategy, test code, code review
"""

from __future__ import annotations

import json
from typing import Any

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from typing_extensions import TypedDict

from agents.bmad.architect import ArchitectAgent
from agents.bmad.developer import DeveloperAgent
from agents.bmad.qa import QAAgent
from agents.bmad.product_manager import ProductManagerAgent
from loaders.personality_loader import load_agent_personality, extract_agent_name
from loaders.skills_loader import load_agent_skills

# ── Shared state ─────────────────────────────────────────────────────────────

class BMadState(TypedDict):
    """State shared across all nodes in the BMad graph."""
    messages: list[dict[str, str]]   # [{role, content}, ...]
    next_agent: str                  # name of the next agent to call, or "FINISH"
    final_response: str              # accumulated final answer

# ── Agent names ───────────────────────────────────────────────────────────────

_AGENT_NAMES: list[str] = [
    "product_manager",
    "architect",
    "developer",
    "qa",
    "FINISH",
]

def _build_supervisor_system() -> str:
    personality = load_agent_personality("orchestrator")
    skills = load_agent_skills("orchestrator")
    return f"""{personality}

---

## Skills & Knowledge Base

{skills}

---

## Team
- **product_manager** – requirements analysis, business analysis, epics, user stories, acceptance criteria, backlog, prioritisation, roadmap
- **architect**       – system design, technical decisions, architecture decision records
- **developer**       – autonomous coding agent (Ravita) that can read/write files and run commands
- **qa**              – testing strategy, test code generation, and code review

Given the conversation so far, decide which agent should respond next, or output \
"FINISH" if the task is fully complete and no more agents are needed.

## Routing rules
1. Route to **product_manager** for requirement gathering, business analysis, user story writing, creating epics, backlog management, prioritisation, or roadmap planning.
2. Route to **architect** for system design, technology choices, or architectural review.
3. Route to **developer** for writing/modifying code, running commands, or fixing bugs.
4. Route to **qa** for writing tests, reviewing code quality, or running test suites.
5. Output "FINISH" only when the user's full request has been addressed.

Respond with a JSON object: {{"next": "<agent_name_or_FINISH>", "reason": "<brief explanation>"}}
"""


_SUPERVISOR_SYSTEM = _build_supervisor_system()


class BMadOrchestrator:
    """Supervisor that routes user requests to the appropriate BMad agent."""

    def __init__(
        self,
        vendor: str,
        api_key: str,
        model: str,
        workspace_path: str,
        verbose: bool = False,
    ) -> None:
        self.verbose = verbose
        self.name = extract_agent_name(load_agent_personality("orchestrator"))

        # Initialise all specialised agents
        self._agents: dict[str, Any] = {
            "product_manager": ProductManagerAgent(vendor, api_key, model, verbose),
            "architect": ArchitectAgent(vendor, api_key, model, verbose),
            "developer": DeveloperAgent(vendor, api_key, model, workspace_path, verbose),
            "qa": QAAgent(vendor, api_key, model, verbose),
        }

        # Supervisor LLM (used only for routing decisions, no tools needed)
        from agents.base_agent import _build_llm
        supervisor_llm = _build_llm(
            vendor=vendor,
            api_key=api_key,
            model=model,
            max_tokens=512,
        )
        self._supervisor_llm = supervisor_llm

        self._graph = self._build_graph()
        self._history: list[dict[str, str]] = []

    # ── Graph construction ───────────────────────────────────────────────────

    def _build_graph(self) -> Any:
        graph = StateGraph(BMadState)

        # Supervisor node decides routing
        graph.add_node("supervisor", self._supervisor_node)

        # One node per specialised agent
        for name in self._agents:
            graph.add_node(name, self._make_agent_node(name))

        # Entry point
        graph.set_entry_point("supervisor")

        # After supervisor: route to chosen agent or end
        graph.add_conditional_edges(
            "supervisor",
            lambda state: state["next_agent"],
            {name: name for name in self._agents} | {"FINISH": END},
        )

        # After any agent: always return to supervisor
        for name in self._agents:
            graph.add_edge(name, "supervisor")

        return graph.compile()

    # ── Node implementations ─────────────────────────────────────────────────

    def _supervisor_node(self, state: BMadState) -> BMadState:
        """Ask the supervisor LLM which agent to call next."""
        messages = state["messages"]
        history_text = "\n".join(
            f"{m['role'].upper()}: {m['content']}" for m in messages
        )

        resp = self._supervisor_llm.invoke([
            SystemMessage(content=_SUPERVISOR_SYSTEM),
            HumanMessage(content=f"Conversation so far:\n\n{history_text}\n\nWhich agent should act next?"),
        ])

        raw = resp.content if isinstance(resp.content, str) else str(resp.content)

        # Parse the JSON routing decision
        try:
            # Strip any markdown code fences
            clean = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            decision = json.loads(clean)
            next_agent = decision.get("next", "FINISH")
            reason = decision.get("reason", "")
        except (json.JSONDecodeError, AttributeError):
            next_agent = "FINISH"
            reason = "Could not parse routing decision"

        if next_agent not in _AGENT_NAMES:
            next_agent = "FINISH"

        if self.verbose:
            print(f"[orchestrator] → {next_agent}  ({reason})")

        return {**state, "next_agent": next_agent}

    def _make_agent_node(self, agent_name: str):
        """Return a LangGraph node function for the named agent."""
        def node(state: BMadState) -> BMadState:
            agent = self._agents[agent_name]
            last_user_msg = ""
            for m in reversed(state["messages"]):
                if m["role"] == "user":
                    last_user_msg = m["content"]
                    break

            if self.verbose:
                print(f"[{agent_name}] processing request...")

            response = agent.invoke(last_user_msg, history=state["messages"][:-1])

            new_messages = state["messages"] + [
                {"role": "assistant", "content": f"[{agent.name}]: {response}"}
            ]
            return {**state, "messages": new_messages, "final_response": response}

        node.__name__ = agent_name
        return node

    # ── Public interface ─────────────────────────────────────────────────────

    def chat(self, user_message: str) -> str:
        """Send a message through the BMad multi-agent pipeline and return the reply."""
        self._history.append({"role": "user", "content": user_message})

        initial_state: BMadState = {
            "messages": list(self._history),
            "next_agent": "supervisor",
            "final_response": "",
        }

        result = self._graph.invoke(initial_state)

        final = result.get("final_response", "(no response)")
        self._history.append({"role": "assistant", "content": final})
        return final

    def reset(self) -> None:
        """Clear conversation history."""
        self._history = []
