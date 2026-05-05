"""BMad QA agent – testing strategy, test code generation, and code review."""

from agents.base_agent import BaseRavitaAgent
from loaders.personality_loader import load_agent_personality, extract_agent_name
from loaders.skills_loader import load_agent_skills
from tools.file_tools import read_file, list_files, repo_map, write_file
from tools.code_tools import analyze_code
from tools.command_tools import execute_command
from tools.git_tools import git_diff, git_status


def _build_qa_prompt(personality: str | None = None) -> str:
    if personality is None:
        personality = load_agent_personality("qa")
    skills = load_agent_skills("qa")
    return f"""{personality}

---

## Skills & Knowledge Base

{skills}

---

## Tools Available
You can read files, analyse code, run commands (to execute test suites), and \
inspect git diffs to review changes before they are merged.

## BMad Process
- Quality is everyone's responsibility, but you are the final gate.
- A story is not done until it has passing tests that cover the acceptance criteria.
- Prefer automated tests over manual verification.
- Follow the testing pyramid: many unit tests, fewer integration tests, fewest e2e.

## Artifact Generation
Whenever you create substantial QA artifacts (test plans, test strategies, test cases, code review reports, quality assessments), automatically save them as markdown files in the `results/qa/` directory. Use task-based naming like `test_plan_authentication_2026-04-14.md` or `code_review_api_endpoints_2026-04-14.md`. Only save the artifact content, not conversation history.
"""


class QAAgent(BaseRavitaAgent):
    """BMad QA: testing strategy, test code generation, and code review."""

    def __init__(
        self,
        vendor: str,
        api_key: str,
        model: str,
        verbose: bool = False,
    ) -> None:
        personality = load_agent_personality("qa")
        super().__init__(
            vendor=vendor,
            api_key=api_key,
            model=model,
            system_prompt=_build_qa_prompt(personality),
            tools=[read_file, list_files, repo_map, analyze_code, execute_command, git_diff, git_status, write_file],
            verbose=verbose,
            name=extract_agent_name(personality),
        )
