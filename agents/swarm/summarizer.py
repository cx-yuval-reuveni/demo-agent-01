from strands import Agent, tool
from agents.config_base_model import get_base_model  # absolute import for package execution
import os
from mcp import StdioServerParameters, stdio_client
from strands.tools.mcp import MCPClient
from dotenv import load_dotenv
load_dotenv()
# Define a specialized system prompt
SUMMARIZER_ASSISTANT_PROMPT = """
You are a specialized summarizer assistant that gets file content and produces concise summaries.
you have access to github mcp server to retrieve file contents from GitHub repositories.
When given a user query, generate a concise summary of the provided content.
"""

def github_server_params() -> StdioServerParameters:
    github_token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")    
    if not github_token:
        raise ValueError("GITHUB_PERSONAL_ACCESS_TOKEN environment variable is required")
    return StdioServerParameters(
        command="docker",
        args=[
            "run",
            "-i",
            "--rm",
            "-e",
            "GITHUB_PERSONAL_ACCESS_TOKEN",
            "ghcr.io/github/github-mcp-server"
        ],
        env={"GITHUB_PERSONAL_ACCESS_TOKEN": github_token}
    )

@tool
def summarizer_assistant(query) -> str:
    """
    Process and respond to summarization-related queries.

    Args:
        query: str: The input query requiring summarization.

    Returns:    
        A concise summary of the provided content
    """
    model = get_base_model()
    github_mcp_client = MCPClient(lambda: stdio_client(github_server_params()))
    with github_mcp_client:
        tools = github_mcp_client.list_tools_sync()
        try:
            # Strands Agents SDK makes it easy to create a specialized agent
            summarizer_agent = Agent(
                system_prompt=SUMMARIZER_ASSISTANT_PROMPT,
                model=model,
                tools=tools,
            )

            # Call the agent and return its response
            response = summarizer_agent(query)
            return str(response)
        except Exception as e:
            return f"Error in summarizer assistant: {str(e)}"