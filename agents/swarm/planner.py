from strands import Agent
from summarizer import summarizer_assistant
from ..config_base_model import get_base_model
from mcp import StdioServerParameters, stdio_client
import os
from strands.tools.mcp import MCPClient

# add langfuse telemetry if env vars are set


MAIN_SYSTEM_PROMPT = """
You are a swarm planner agent that delegates tasks to specialized assistants.
You have access to the following specialized assistants:
1. Summarizer Assistant: Use this assistant to generate concise summaries of file content.
You have access to github mcp_tool to retrieve file contents from GitHub repositories.
When given a user query, determine if it requires summarization.
If it does, delegate the task to the Summarizer Assistant.
Always provide clear instructions to the specialized assistant about what needs to be summarized."""

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

github_mcp_client = MCPClient(lambda: stdio_client(github_server_params()))
with github_mcp_client:
    tools = github_mcp_client.list_tools_sync() + [summarizer_assistant]
    repo_path = "cx-yuval-reuveni/demo-agent-01"
    repo_name = repo_path.split("/")[-1]
    planner_agent = Agent(
        system_prompt=MAIN_SYSTEM_PROMPT,
        tools=tools,
        model=get_base_model(),
        trace_attributes={
            "session.id": f"second-github-agent-session-",
            "user.id": "yuval.reuveni@checkmarx.com",
            "repo.name": repo_name
    },

)