"""BMad Developer agent – Ravita, the autonomous coding agent with full toolset."""

from agents.base_agent import BaseRavitaAgent
from loaders.personality_loader import load_agent_personality, extract_agent_name
from loaders.skills_loader import load_agent_skills
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


def _build_developer_prompt(workspace_path: str, personality: str | None = None) -> str:
    if personality is None:
        personality = load_agent_personality("developer")
    skills = load_agent_skills("developer")
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

## BMad Role
You are the **Developer** in the BMad Agile AI-Driven Development framework. \
You implement features, fix bugs, and refactor code based on specifications \
produced by the Product Manager and Architect agents. Always validate your changes by \
running tests and linters when available.

## Artifact Generation
Whenever you create substantial development artifacts (implementation docs, technical notes, code design documents, deployment guides), automatically save them as markdown files in the `results/developer/` directory. Use task-based naming like `implementation_jwt_auth_2026-04-14.md` or `deployment_guide_microservice_2026-04-14.md`. Only save the artifact content, not conversation history.
"""


class DeveloperAgent(BaseRavitaAgent):
    """BMad Developer: Ravita, the autonomous coding agent with all tools."""

    def __init__(
        self,
        vendor: str,
        api_key: str,
        model: str,
        workspace_path: str,
        verbose: bool = False,
    ) -> None:
        personality = load_agent_personality("developer")
        super().__init__(
            vendor=vendor,
            api_key=api_key,
            model=model,
            system_prompt=_build_developer_prompt(workspace_path, personality),
            tools=_ALL_TOOLS,
            verbose=verbose,
            name=extract_agent_name(personality),
        )
