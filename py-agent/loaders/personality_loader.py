"""Loads agent personality from the personality/ directory."""

import re
from pathlib import Path

_PERSONALITY_DIR = Path(__file__).parent.parent / "personality"
_PERSONALITY_FILE = _PERSONALITY_DIR / "personality.md"


def load_personality() -> str:
    """Read and return the personality prompt from personality.md (default developer personality)."""
    try:
        return _PERSONALITY_FILE.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"Personality file not found: {_PERSONALITY_FILE}"
        ) from exc


def extract_agent_name(personality_text: str) -> str:
    """Extract the agent's display name from its personality markdown.

    Looks for the pattern ``You are **<Name>**`` which every personality file
    uses to declare the agent's identity.  Returns ``"Agent"`` as a fallback
    if no match is found.

    Args:
        personality_text: The full content of a personality markdown file.

    Returns:
        The agent's display name, or ``"Agent"`` if no name can be extracted.
    """
    match = re.search(r'You are \*\*([^*]+)\*\*', personality_text)
    if match:
        return match.group(1).strip()
    return "Agent"


def load_agent_personality(agent_name: str) -> str:
    """Read and return the personality prompt for the named agent.

    Looks for ``<agent_name>_personality.md`` in the personality/ directory.
    Falls back to the default ``personality.md`` if no agent-specific file exists.

    Args:
        agent_name: One of ``architect``, ``developer``,
                    ``orchestrator``, ``qa``, ``product_manager``.
    """
    agent_file = _PERSONALITY_DIR / f"{agent_name}_personality.md"
    if agent_file.exists():
        return agent_file.read_text(encoding="utf-8")
    # Graceful fallback to the generic personality
    return load_personality()
