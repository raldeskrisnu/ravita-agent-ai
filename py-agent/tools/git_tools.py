"""Git tools: git_status, git_diff, git_log."""

import subprocess

from langchain_core.tools import tool

import tools.file_tools as _file_tools


def _run_git(*args: str) -> str:
    """Run a git sub-command in the workspace directory and return output."""
    workspace = _file_tools._WORKSPACE_ROOT
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = result.stdout.strip()
        if result.returncode != 0:
            stderr = result.stderr.strip()
            return f"ERROR: git {' '.join(args)} failed\n{stderr}"
        return output if output else "(no output)"
    except subprocess.TimeoutExpired:
        return f"ERROR: git {' '.join(args)} timed out"
    except Exception as exc:
        return f"ERROR: {exc}"


@tool
def git_status() -> str:
    """Run 'git status' in the workspace to see which files have been modified,
    staged, or are untracked."""
    return _run_git("status", "--short", "--branch")


@tool
def git_diff(ref: str | None = None) -> str:
    """Show the diff of changes in the workspace.

    Args:
        ref: Optional git ref (branch, commit, tag) to diff against.
             Defaults to showing uncommitted working-tree changes.
    """
    if ref:
        return _run_git("diff", ref)
    return _run_git("diff")


@tool
def git_log(n: int = 10) -> str:
    """Show the recent commit history of the workspace repository.

    Args:
        n: Number of commits to show. Defaults to 10.
    """
    if n <= 0:
        n = 10
    return _run_git("log", f"--max-count={n}", "--oneline", "--decorate")
