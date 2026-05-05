"""Shell command execution tool: execute_command."""

import subprocess

from langchain_core.tools import tool

import tools.file_tools as _file_tools


@tool
def execute_command(command: str, timeout_seconds: int = 30) -> str:
    """Execute a shell command inside the workspace directory.
    Use this to run build commands, tests, linters, scripts, or to compile and
    execute code. Commands run with the workspace as the current working directory.

    Args:
        command: The shell command to run (executed via /bin/sh -c).
        timeout_seconds: Maximum seconds to wait for the command to finish.
                         Defaults to 30.
    """
    if timeout_seconds <= 0:
        timeout_seconds = 30

    workspace = _file_tools._WORKSPACE_ROOT
    try:
        result = subprocess.run(
            ["/bin/sh", "-c", command],
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )

        parts: list[str] = []
        if result.stdout.strip():
            parts.append(f"STDOUT:\n{result.stdout.rstrip()}")
        if result.stderr.strip():
            parts.append(f"STDERR:\n{result.stderr.rstrip()}")
        if result.returncode != 0:
            parts.append(f"EXIT CODE: {result.returncode}")

        return "\n\n".join(parts) if parts else "(no output)"

    except subprocess.TimeoutExpired:
        return f"ERROR: Command timed out after {timeout_seconds} seconds"
    except Exception as exc:
        return f"ERROR executing command: {exc}"
