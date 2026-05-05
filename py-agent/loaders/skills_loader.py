"""Loads skill markdown files from the skills/ directory."""

from pathlib import Path

_SKILLS_DIR = Path(__file__).parent.parent / "skills"


def load_skills() -> str:
    """Read all *.md files in the skills/ directory, sorted alphabetically,
    and return them as a single concatenated string with section headers."""
    if not _SKILLS_DIR.is_dir():
        raise FileNotFoundError(f"Skills directory not found: {_SKILLS_DIR}")

    md_files = sorted(_SKILLS_DIR.glob("*.md"))
    if not md_files:
        raise FileNotFoundError(f"No .md skill files found in {_SKILLS_DIR}")

    sections: list[str] = []
    for md_file in md_files:
        section_name = md_file.stem
        content = md_file.read_text(encoding="utf-8")
        sections.append(f"### {section_name}\n\n{content}")

    return "\n\n".join(sections)


def load_agent_skills(agent_name: str) -> str:
    """Read and return the skills for the named agent.

    Looks for ``<agent_name>_skills.md`` in the skills/ directory.
    Falls back to loading all skills if no agent-specific file exists.

    Args:
        agent_name: One of ``architect``, ``developer``,
                    ``orchestrator``, ``qa``, ``product_manager``.
    """
    agent_file = _SKILLS_DIR / f"{agent_name}_skills.md"
    if agent_file.exists():
        return agent_file.read_text(encoding="utf-8")
    # Graceful fallback to the full skills set
    return load_skills()
