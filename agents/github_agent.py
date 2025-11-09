import os
from mcp import StdioServerParameters, stdio_client
from strands import Agent
from strands.tools.mcp import MCPClient
from dotenv import load_dotenv
from config_base_model import get_base_model
from langfuse import get_client as get_langfuse_client
from langfuse import observe, get_client
import base64
import numpy as np


load_dotenv()


# 1. Define the parameters for starting the local GitHub MCP server via Docker
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
 
async def run_task(agent, repo_path, random_session):
    repo_name = repo_path.split("/")[-1]
    prompt = (
        f"Phase 1: List important files in https://github.com/{repo_path}. "
        f"Phase 2: Summarize their purpose. "
        f"Phase 3: Draft a concise README with install + run steps for the GitHub agent. "
        f"Name output file: README for repo {repo_name} session {random_session}.md "
        f"Return final README content directly; do not attempt to write the file."
    )
    return agent(prompt)

# Use the agent with a prompt that requires a GitHub action

async def main():
    random_session = np.random.randint(0,1000)

    public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY")
    if public_key and secret_key:
        LANGFUSE_AUTH = base64.b64encode(f"{public_key}:{secret_key}".encode()).decode()
        os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {LANGFUSE_AUTH}"
        from strands.telemetry import StrandsTelemetry
        # Configure the telemetry
        # (Creates new tracer provider and sets it as global)
        strands_telemetry = StrandsTelemetry().setup_otlp_exporter()

    model = get_base_model(max_tokens=8000)

    github_mcp_client = MCPClient(lambda: stdio_client(github_server_params()))
    with github_mcp_client:
        tools = github_mcp_client.list_tools_sync()
        repo_path = "cx-yuval-reuveni/demo-agent-01"
        repo_name = repo_path.split("/")[-1]
        agent = Agent(
            model=model,
            tools=tools,
            system_prompt="You are a helpful GitHub assistant that uses available tools to answer questions.",
            trace_attributes={
                "session.id": f"first-github-agent-session-{random_session}",
                "user.id": "yuval.reuveni@checkmarx.com",
                "repo.name": repo_name
            },
        )
        try:
            result = agent(
                f"Analyze https://github.com/{repo_path} and create a README with setup (uv, make), "
                f"environment variables, how to run this github_agent, GitHub MCP usage (manual vs managed), "
                f"troubleshooting (network errors). Name the file: 'README for repo {repo_name} session {random_session}.md'. "
                f"Save the readme file in READMEs folder."
            )
            print(result)
        except Exception as e:
            print(f"[error] agent invocation failed: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())