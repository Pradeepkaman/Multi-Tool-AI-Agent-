"""Real-time web search tool using DuckDuckGo."""

import warnings
from typing import List, Dict
from langchain_core.tools import tool

# Suppress harmless package renaming notice
warnings.filterwarnings("ignore")

try:
    from ddgs import DDGS
except ImportError:
    try:
        from duckduckgo_search import DDGS
    except ImportError:
        DDGS = None


def search_web(query: str, max_results: int = 5) -> str:
    """Searches the web in real-time via DuckDuckGo and formats the results.

    Args:
        query: The search query string.
        max_results: Maximum number of search results to retrieve (default: 5).

    Returns:
        Formatted summary of search results with titles, snippets, and URLs.
    """
    clean_query = query.strip().strip("'\"")
    if not clean_query:
        return "Error: Empty search query provided."

    if DDGS is None:
        return "Error: DuckDuckGo search library is not installed."

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            ddgs = DDGS()
            results = list(ddgs.text(clean_query, max_results=max_results))

        if not results:
            return f"No web search results found for query: '{clean_query}'."

        formatted_output = [f"Web Search Results for '{clean_query}':\n"]
        for idx, item in enumerate(results, 1):
            title = item.get("title", "No Title")
            snippet = item.get("body", "No description available.")
            link = item.get("href", "")
            formatted_output.append(f"{idx}. {title}\n   Snippet: {snippet}\n   URL: {link}\n")

        return "\n".join(formatted_output).strip()

    except Exception as exc:
        return f"Error executing web search for '{clean_query}': {str(exc)}"


@tool("web_search")
def web_search_tool(query: str) -> str:
    """Useful for searching the public web for real-time information, current facts, definitions, news, and external data.
    Input should be a specific search query string like 'current inflation rate 2024' or 'Python 3.12 release date'.
    """
    return search_web(query)
