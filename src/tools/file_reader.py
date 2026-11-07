"""Local file reader tool for inspecting files within the project/workspace."""

import os
from pathlib import Path
from langchain_core.tools import tool


# Base project directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent


def read_file_content(file_path: str, max_chars: int = 8000) -> str:
    """Reads content from a local file safely.

    Args:
        file_path: Path to the target file (relative or absolute).
        max_chars: Maximum characters to return to prevent overflowing context.

    Returns:
        The content of the file or an error message.
    """
    if not file_path or not file_path.strip():
        return "Error: No file path provided."

    target_path = Path(file_path.strip())

    # If relative, resolve relative to project base directory
    if not target_path.is_absolute():
        target_path = (BASE_DIR / target_path).resolve()
    else:
        target_path = target_path.resolve()

    if not target_path.exists():
        return f"Error: File not found at '{file_path}' (resolved: '{target_path}')."

    if not target_path.is_file():
        return f"Error: Path '{file_path}' is a directory, not a file."

    try:
        content = target_path.read_text(encoding="utf-8", errors="replace")
        total_len = len(content)

        if total_len > max_chars:
            truncated = content[:max_chars]
            return (
                f"[File: {target_path.name} ({total_len} chars total, showing first {max_chars} chars)]:\n\n"
                f"{truncated}\n\n... [Truncated for brevity]"
            )

        return f"[File: {target_path.name}]:\n\n{content}"

    except Exception as exc:
        return f"Error reading file '{file_path}': {str(exc)}"


@tool("read_local_file")
def file_reader_tool(file_path: str) -> str:
    """Useful for reading the contents of a local file (such as notes, data files, reports, markdown, CSV, or text).
    Input must be a valid relative or absolute file path string like 'data/company_notes.txt' or 'README.md'.
    """
    return read_file_content(file_path)

