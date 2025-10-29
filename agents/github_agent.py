from strands import Agent
import os
from dotenv import load_dotenv
import subprocess
import json
from agent_tools.github_tools import (
    mcp_get_repository, 
    mcp_search_repositories, 
    mcp_get_file_contents,
    mcp_list_tools,
    mcp_create_issue,
    mcp_get_issues
)
from .config_base_model import get_base_model

load_dotenv()

def create_github_agent():
    """Create and return the GitHub MCP agent"""
    model = get_base_model(max_tokens=30000)
    
    gh_agent = Agent(
        model=model,
        tools=[
            mcp_get_repository, 
            mcp_search_repositories, 
            mcp_get_file_contents,
            mcp_list_tools,
            mcp_create_issue,
            mcp_get_issues
        ],
        system_prompt="""You are a GitHub analysis agent using Docker-based MCP (Model Context Protocol).
            
            You have access to these MCP tools:
            1. mcp_get_repository(owner, repo) - Get detailed repository information
            2. mcp_search_repositories(query, limit) - Search for repositories  
            3. mcp_get_file_contents(owner, repo, path) - Get contents of specific files
            4. mcp_list_tools() - List all available MCP tools
            5. mcp_create_issue(owner, repo, title, body) - Create issues in repositories
            6. mcp_get_issues(owner, repo, state, limit) - Get repository issues

            Your job is to:
            - Analyze repositories using Docker-based MCP tools
            - Create comprehensive README files
            - Provide insights about repository structure and content
            - Manage GitHub issues when requested
            - Always mention that you're using Docker-based MCP protocol for data access

            When analyzing a repository, first get its basic info, then look at key files like README.md, package.json, requirements.txt, etc.
            
            The MCP server runs in a Docker container and provides real-time access to GitHub's API."""
        )
    
    return gh_agent

def main():
    """Main function for CLI usage"""
    print("=== Testing MCP GitHub Agent ===")
    
    # Create the agent
    github_agent = create_github_agent()
    
    # Test the agent
    response = github_agent("Do not use any tool just say hi to confirm you are working with the GitHub MCP agent.")
    print(response)
    return response


# This block only runs when the file is executed directly
if __name__ == "__main__":
    main()