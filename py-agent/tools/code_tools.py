"""Code analysis tool: analyze_code."""

from langchain_core.tools import tool

import tools.file_tools as _file_tools


@tool
def analyze_code(path: str, question: str) -> str:
    """Read and analyse a source file, then answer a specific question about it.
    Use this to understand the current implementation, find patterns, detect
    issues, or reason about architecture before making changes.

    Args:
        path: Path to the file to analyse (relative to workspace root or absolute).
        question: The specific question to answer about the code.
    """
    try:
        abs_path = _file_tools._resolve_path(_file_tools._WORKSPACE_ROOT, path)
        content = abs_path.read_text(encoding="utf-8")
        return f"File: {path}\nQuestion: {question}\n\n---\n\n{content}"
    except ValueError as exc:
        return f"ERROR: {exc}"
    except FileNotFoundError:
        return f"ERROR: File not found: {path}"
    except Exception as exc:
        return f"ERROR analysing file '{path}': {exc}"
