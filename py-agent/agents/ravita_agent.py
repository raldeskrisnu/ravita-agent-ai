"""Ravita single-agent: the autonomous coding agent powered by LangChain + Claude."""

from __future__ import annotations

from typing import Any

from agents.base_agent import BaseRavitaAgent
from loaders.personality_loader import load_personality, extract_agent_name
from loaders.skills_loader import load_skills
from tools.file_tools import read_file, write_file, list_files, repo_map
from tools.git_tools import git_status, git_diff, git_log
from tools.code_tools import analyze_code
from tools.command_tools import execute_command

_ALL_TOOLS = [
    read_file,
    write_file,
    list_files,
    repo_map,
    git_status,
    git_diff,
    git_log,
    analyze_code,
    execute_command,
]


def _build_system_prompt(workspace_path: str, personality: str | None = None) -> str:
    if personality is None:
        personality = load_personality()
    skills = load_skills()
    return f"""{personality}

---

## Skills & Knowledge Base

{skills}

---

## Workspace
Your active workspace is located at: {workspace_path}

When reading or writing files, always use paths relative to the workspace root \
or absolute paths within the workspace.
Always think step-by-step before acting. Use tools to gather information before \
making changes.
After every significant action, reflect on the result and decide the next best step.

## Conversational style
- For short factual questions, reply concisely (1-3 sentences or a short list).
- Reserve detailed explanations and code blocks for tasks that genuinely need them.
- When unsure what the user wants, ask one clarifying question instead of assuming.
"""


class RavitaAgent:
    """Autonomous coding agent with conversation history and full toolset."""

    def __init__(
        self,
        vendor: str,
        api_key: str,
        model: str,
        workspace_path: str,
        verbose: bool = False,
    ) -> None:
        self.verbose = verbose
        self._history: list[dict[str, Any]] = []
        personality_text = load_personality()
        self.name = extract_agent_name(personality_text)
        self._agent = BaseRavitaAgent(
            vendor=vendor,
            api_key=api_key,
            model=model,
            system_prompt=_build_system_prompt(workspace_path, personality_text),
            tools=_ALL_TOOLS,
            verbose=verbose,
            name=self.name,
        )

    def chat(self, user_message: str) -> str:
        """Send *user_message* to Ravita and return her response.
        Maintains conversation history across calls.
        """
        response = self._agent.invoke(user_message, history=self._history)

        self._history.append({"role": "user", "content": user_message})
        self._history.append({"role": "assistant", "content": response})

        return response

    def reset(self) -> None:
        """Clear conversation history."""
        self._history = []
