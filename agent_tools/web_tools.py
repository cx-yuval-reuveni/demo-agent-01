from strands.tools import tool
from ddgs import DDGS

@tool
def web_search(query: str) -> str:
    """
    Searches the web for the given query using DuckDuckGo and returns the results.
    Use this to find current information, news, or answer questions about topics you don't know about.
    """
    with DDGS() as ddgs:
        results = [r for r in ddgs.text(query, max_results=5)]
        return str(results) if results else "No results found."
