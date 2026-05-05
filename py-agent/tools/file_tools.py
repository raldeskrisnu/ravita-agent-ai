"""File system tools: read_file, write_file, list_files, repo_map."""

import os
from pathlib import Path

from langchain_core.tools import tool


def _resolve_path(workspace_root: str, path: str) -> Path:
    """Resolve *path* relative to *workspace_root*, preventing path traversal."""
    root = Path(workspace_root).resolve()
    if Path(path).is_absolute():
        resolved = Path(path).resolve()
    else:
        resolved = (root / path).resolve()

    if not str(resolved).startswith(str(root)):
        raise ValueError(f"Path '{path}' is outside the workspace root")

    return resolved


# The workspace root is injected at startup via a module-level variable so that
# the @tool functions (which must have a fixed signature) can access it.
_WORKSPACE_ROOT: str = "."


def set_workspace(path: str) -> None:
    """Set the global workspace root used by all file tools."""
    global _WORKSPACE_ROOT
    _WORKSPACE_ROOT = path


@tool
def read_file(path: str) -> str:
    """Read the full contents of a file.

    Args:
        path: Path to the file (relative to workspace root or absolute).
    """
    try:
        abs_path = _resolve_path(_WORKSPACE_ROOT, path)
        return abs_path.read_text(encoding="utf-8")
    except ValueError as exc:
        return f"ERROR: {exc}"
    except FileNotFoundError:
        return f"ERROR: File not found: {path}"
    except Exception as exc:
        return f"ERROR reading file '{path}': {exc}"


@tool
def write_file(path: str, content: str) -> str:
    """Create or overwrite a file with the provided content.
    Parent directories are created automatically.

    Args:
        path: Path to the file to write (relative to workspace root or absolute).
        content: Full content to write to the file.
    """
    try:
        abs_path = _resolve_path(_WORKSPACE_ROOT, path)
        abs_path.parent.mkdir(parents=True, exist_ok=True)
        abs_path.write_text(content, encoding="utf-8")
        return f"File written successfully: {abs_path} ({len(content)} bytes)"
    except ValueError as exc:
        return f"ERROR: {exc}"
    except Exception as exc:
        return f"ERROR writing file '{path}': {exc}"


@tool
def list_files(path: str | None = None) -> str:
    """List all files and directories inside a directory.

    Args:
        path: Directory path to list (relative to workspace root or absolute).
              Defaults to the workspace root.
    """
    try:
        target = path if path else _WORKSPACE_ROOT
        abs_path = _resolve_path(_WORKSPACE_ROOT, target)

        if not abs_path.is_dir():
            return f"ERROR: '{path}' is not a directory"

        lines = [f"Contents of {abs_path}:"]
        for entry in sorted(abs_path.iterdir(), key=lambda e: (not e.is_dir(), e.name)):
            if entry.is_dir():
                lines.append(f"  [DIR]  {entry.name}")
            else:
                lines.append(f"  [FILE] {entry.name}  ({entry.stat().st_size} bytes)")

        return "\n".join(lines)
    except ValueError as exc:
        return f"ERROR: {exc}"
    except Exception as exc:
        return f"ERROR listing files: {exc}"


_IGNORED_DIRS = {
    "node_modules", "vendor", ".git", "dist", "build",
    "__pycache__", ".idea", ".vscode", "target", ".cache",
    ".mypy_cache", ".pytest_cache", ".ruff_cache", "venv", ".venv",
}


def _build_tree(directory: Path, prefix: str, depth: int, max_depth: int) -> list[str]:
    if depth >= max_depth:
        return [prefix + "..."]

    try:
        entries = [
            e for e in sorted(directory.iterdir(), key=lambda e: (not e.is_dir(), e.name))
            if not e.name.startswith(".")
            and not (e.is_dir() and e.name in _IGNORED_DIRS)
        ]
    except PermissionError:
        return [prefix + "[permission denied]"]

    lines: list[str] = []
    for i, entry in enumerate(entries):
        last = i == len(entries) - 1
        connector = "└── " if last else "├── "
        child_prefix = prefix + ("    " if last else "│   ")
        lines.append(f"{prefix}{connector}{entry.name}")
        if entry.is_dir():
            lines.extend(_build_tree(entry, child_prefix, depth + 1, max_depth))

    return lines


@tool
def repo_map(path: str | None = None) -> str:
    """Generate a tree-style map of a directory showing its structure.

    Args:
        path: Root path to map (relative to workspace root or absolute).
              Defaults to workspace root.
    """
    try:
        target = path if path else _WORKSPACE_ROOT
        abs_path = _resolve_path(_WORKSPACE_ROOT, target)

        if not abs_path.is_dir():
            return f"ERROR: '{path}' is not a directory"

        lines = [str(abs_path)] + _build_tree(abs_path, "", 0, 6)
        return "\n".join(lines)
    except ValueError as exc:
        return f"ERROR: {exc}"
    except Exception as exc:
        return f"ERROR building repo map: {exc}"
