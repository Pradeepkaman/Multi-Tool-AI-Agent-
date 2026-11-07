"""Tools export registry."""

from src.tools.calculator import calculator_tool, safe_calculate
from src.tools.file_reader import file_reader_tool, read_file_content
from src.tools.search import web_search_tool, search_web

ALL_TOOLS = [
    web_search_tool,
    calculator_tool,
    file_reader_tool,
]

TOOLS_BY_NAME = {tool.name: tool for tool in ALL_TOOLS}

__all__ = [
    "calculator_tool",
    "safe_calculate",
    "file_reader_tool",
    "read_file_content",
    "web_search_tool",
    "search_web",
    "ALL_TOOLS",
    "TOOLS_BY_NAME",
]
