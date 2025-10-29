"""
Demo Agent 01 - AI Agent using Docker-based MCP for GitHub integration
"""

__version__ = "0.1.0"
__author__ = "Yuval Reuveni"
__email__ = "yuval.reuveni@checkmarx.com"

from .agents.github_agent import create_github_agent
from .agent_tools.github_tools import (
    mcp_get_repository,
    mcp_search_repositories, 
    mcp_get_file_contents,
    mcp_list_tools,
    mcp_create_issue,
    mcp_get_issues,
)

__all__ = [
    "create_github_agent",
    "mcp_get_repository",
    "mcp_search_repositories", 
    "mcp_get_file_contents",
    "mcp_list_tools",
    "mcp_create_issue",
    "mcp_get_issues",
]