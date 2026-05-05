"""BMad Product Manager agent – backlog management, prioritisation, roadmap."""

from agents.base_agent import BaseRavitaAgent
from loaders.personality_loader import load_agent_personality, extract_agent_name
from loaders.skills_loader import load_agent_skills
from tools.file_tools import write_file


def _build_pm_prompt(personality: str | None = None) -> str:
    if personality is None:
        personality = load_agent_personality("product_manager")
    skills = load_agent_skills("product_manager")
    return f"""{personality}

---

## Skills & Knowledge Base

{skills}

---

## BMad Process
- Start every new feature or initiative with requirements analysis: ask clarifying questions, understand the business goal, and document assumptions.
- Decompose business goals into Epics with measurable success criteria (KPIs/OKRs).
- Break Epics into sprint-sized Stories using the INVEST criteria; write Given/When/Then acceptance criteria for each.
- Maintain a living product roadmap that reflects current priorities.
- Every sprint starts with a clearly defined goal.
- Definition of Done must be agreed before a story enters the sprint.
- Retrospective insights should feed back into the backlog as improvement items.

## Artifact Generation
Whenever you create substantial product artifacts (epics, user stories, product requirements, roadmaps, backlogs), automatically save them as markdown files in the `results/product_manager/` directory. Use task-based naming like `epic_user_authentication_2026-04-14.md` or `backlog_sprint_planning_2026-04-14.md`. Only save the artifact content, not conversation history.
"""


class ProductManagerAgent(BaseRavitaAgent):
    """BMad Product Manager: backlog management, prioritisation, and roadmap."""

    def __init__(
        self,
        vendor: str,
        api_key: str,
        model: str,
        verbose: bool = False,
    ) -> None:
        personality = load_agent_personality("product_manager")
        super().__init__(
            vendor=vendor,
            api_key=api_key,
            model=model,
            system_prompt=_build_pm_prompt(personality),
            tools=[write_file],
            verbose=verbose,
            name=extract_agent_name(personality),
        )
