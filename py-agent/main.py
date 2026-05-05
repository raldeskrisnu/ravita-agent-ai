"""Ravita Agent – Python CLI entry point.

Supports two modes:
  - Single-agent mode (default): Ravita, the autonomous coding agent.
  - BMad multi-agent mode (BMAD_MODE=true): Ravita team orchestrated by BMad
    methodology (Product Manager, Architect, Developer, QA).

Supported AI vendors (AI_VENDOR):
  - claude  → Anthropic Claude (default)
  - gemini  → Google Gemini
  - openai  → OpenAI GPT
"""

import os
import sys

# Allow importing from the py-agent directory as the package root
sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv

load_dotenv()

from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings

from tools.file_tools import set_workspace


def _get_env(key: str, default: str = "") -> str:
    return os.environ.get(key, default)


def _build_prompt_session() -> PromptSession:
    """Create a PromptSession where Enter submits and Shift+Enter inserts a newline."""
    kb = KeyBindings()

    @kb.add("enter")
    def _submit(event) -> None:
        event.current_buffer.validate_and_handle()

    @kb.add("escape", "enter")
    def _newline_alt(event) -> None:
        event.current_buffer.insert_text("\n")

    return PromptSession(multiline=True, key_bindings=kb)


def main() -> None:
    vendor = (_get_env("AI_VENDOR") or "claude").lower()
    api_key = _get_env("API_KEY")
    model = _get_env("AI_MODEL")

    # Vendor-specific model defaults
    _default_models = {
        "claude": "claude-opus-4-5",
        "gemini": "gemini-2.0-flash",
        "openai": "gpt-4o",
    }

    supported_vendors = tuple(_default_models.keys())
    if vendor not in supported_vendors:
        print(
            f'[error] unsupported AI_VENDOR "{vendor}": must be one of {", ".join(supported_vendors)}',
            file=sys.stderr,
        )
        sys.exit(1)

    if not api_key:
        print("[error] API_KEY is not set", file=sys.stderr)
        sys.exit(1)

    if not model:
        model = _default_models[vendor]

    workspace = _get_env("WORKSPACE_PATH") or "./workspace"
    verbose = _get_env("AGENT_VERBOSE", "false").lower() == "true"
    bmad_mode = _get_env("BMAD_MODE", "false").lower() == "true"

    # Resolve workspace path
    workspace = os.path.abspath(workspace)
    os.makedirs(workspace, exist_ok=True)

    # Inject workspace into file tools
    set_workspace(workspace)

    if bmad_mode:
        from agents.bmad.orchestrator import BMadOrchestrator
        agent = BMadOrchestrator(vendor, api_key, model, workspace, verbose)
        mode_label = "BMad Multi-Agent"
    else:
        from agents.ravita_agent import RavitaAgent
        agent = RavitaAgent(vendor, api_key, model, workspace, verbose)
        mode_label = "Single-Agent (Ravita)"

    agent_name = agent.name

    print("╔══════════════════════════════════════════════════╗")
    print("║       Ravita – Autonomous Coding Agent           ║")
    print("╚══════════════════════════════════════════════════╝")
    print(f"Vendor:    {vendor}")
    print(f"Mode:      {mode_label}")
    print(f"Agent:     {agent_name}")
    print(f"Model:     {model}")
    print(f"Workspace: {workspace}")
    print("Type 'exit' or 'quit' to stop. Type 'reset' to clear history.")
    print("Press Enter to send. Press Shift+Enter (or Alt+Enter) for a new line.")
    print()

    session = _build_prompt_session()

    while True:
        try:
            user_input = session.prompt("You > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        if user_input.lower() == "reset":
            agent.reset()
            print("[agent] Conversation history cleared.")
            continue

        try:
            reply = agent.chat(user_input)
            print(f"\n{agent_name} > {reply}\n")
        except Exception as exc:
            print(f"[error] {exc}", file=sys.stderr)


if __name__ == "__main__":
    main()
