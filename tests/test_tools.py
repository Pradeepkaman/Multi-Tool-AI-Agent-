"""Unit verification for agent tools."""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.tools.calculator import safe_calculate, calculator_tool
from src.tools.file_reader import read_file_content, file_reader_tool
from src.tools.search import search_web, web_search_tool


def test_calculator():
    print("[1/3] Testing Calculator Tool...")
    # Basic math
    res = safe_calculate("25 * 4 + 10")
    assert res == "110", f"Expected 110, got {res}"

    # Powers and brackets
    res = safe_calculate("(10 + 5) ** 2")
    assert res == "225", f"Expected 225, got {res}"

    # Math library functions
    res = safe_calculate("sqrt(144) + sin(0)")
    assert res == "12", f"Expected 12, got {res}"

    # Division by zero safety
    res = safe_calculate("10 / 0")
    assert "Division by zero" in res, f"Expected division by zero, got {res}"

    # Code injection safety
    res = safe_calculate("__import__('os').system('dir')")
    assert "Error: Expression contains prohibited keyword" in res, f"Expected prohibited keyword error, got {res}"

    print("  Calculator tool passed all tests!")


def test_file_reader():
    print("[2/3] Testing File Reader Tool...")
    # Test reading existing file
    readme_path = PROJECT_ROOT / "requirements.txt"
    res = read_file_content(str(readme_path))
    assert "langchain-core" in res, f"Expected 'langchain-core' in content, got: {res}"

    # Test missing file error handling
    res = read_file_content("non_existent_file_123.txt")
    assert "Error: File not found" in res, f"Expected file not found error, got: {res}"

    print("  File reader tool passed all tests!")


def test_web_search():
    print("[3/3] Testing Web Search Tool...")
    res = search_web("Python programming language", max_results=2)
    assert "Python" in res, f"Expected 'Python' in search results, got: {res}"
    assert "URL:" in res, f"Expected URLs in search results, got: {res}"

    print("  Web search tool passed all tests!")


if __name__ == "__main__":
    print("=== Running Standalone Tool Verification ===")
    test_calculator()
    test_file_reader()
    test_web_search()
    print("=== All Tool Tests Passed Successfully! ===")

