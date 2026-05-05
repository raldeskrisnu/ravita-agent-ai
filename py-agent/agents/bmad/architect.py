"""BMad Architect agent – system design, technical decisions, ADRs."""

from agents.base_agent import BaseRavitaAgent
from loaders.personality_loader import load_agent_personality, extract_agent_name
from loaders.skills_loader import load_agent_skills
from tools.file_tools import read_file, list_files, repo_map, write_file
from tools.code_tools import analyze_code


def _build_architect_prompt(personality: str | None = None) -> str:
    if personality is None:
        personality = load_agent_personality("architect")
    skills = load_agent_skills("architect")
    return f"""{personality}

---

## Skills & Knowledge Base

{skills}

---

## Tools Available
You can read files and explore the codebase to understand the current architecture \
before making recommendations. Use these tools to ground your decisions in reality.

## BMad Process
- Apply SOLID, DRY, and KISS principles.
- Prefer simple, proven patterns over clever novelty.
- Document trade-offs explicitly so the team can revisit decisions later.

## Artifact Generation
Whenever you create substantial architectural artifacts (ADRs, system designs, technical specifications, architecture diagrams), automatically save them as markdown files in the `results/architect/` directory. Use task-based naming like `adr_jwt_authentication_2026-04-14.md` or `system_design_api_gateway_2026-04-14.md`. Only save the artifact content, not conversation history.
"""


class ArchitectAgent(BaseRavitaAgent):
    """BMad Architect: system design, technical decisions, and ADRs."""

    def __init__(
        self,
        vendor: str,
        api_key: str,
        model: str,
        verbose: bool = False,
    ) -> None:
        personality = load_agent_personality("architect")
        super().__init__(
            vendor=vendor,
            api_key=api_key,
            model=model,
            system_prompt=_build_architect_prompt(personality),
            tools=[read_file, list_files, repo_map, analyze_code, write_file],
            verbose=verbose,
            name=extract_agent_name(personality),
        )
