import os
from mcp import StdioServerParameters, stdio_client
from strands import Agent
from strands.tools.mcp import MCPClient
from dotenv import load_dotenv
from config_base_model import get_base_model
from langfuse import get_client as get_langfuse_client
import base64


load_dotenv()


# 1. Define the parameters for starting the local GitHub MCP server via Docker
def github_server_params() -> StdioServerParameters:
    github_token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")    
    return StdioServerParameters(
        command="docker",
        args=[
            "run",
            "-i",
            "--rm",
            "-e",
            "GITHUB_PERSONAL_ACCESS_TOKEN=" + github_token,
            "ghcr.io/github/github-mcp-server"
        ],
        env={"GITHUB_PERSONAL_ACCESS_TOKEN": github_token}
    )
 


# Use the agent with a prompt that requires a GitHub action

async def main():
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY")
    base_url = os.getenv("LANGFUSE_BASE_URL")

    if public_key and secret_key:
        LANGFUSE_AUTH = base64.b64encode(f"{public_key}:{secret_key}".encode()).decode()
        os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {LANGFUSE_AUTH}"

    from strands.telemetry import StrandsTelemetry
    strands_telemetry = StrandsTelemetry().setup_otlp_exporter()

    model = get_base_model(max_tokens=30000)

    # MCPClient expects a callable that returns a context manager
    github_mcp_client = MCPClient(lambda: stdio_client(github_server_params()))
    agent = Agent(
        model=model,
        system_prompt="You are a helpful GitHub assistant that uses available tools to answer questions.",
        tools=[github_mcp_client],
        trace_attributes={
            "session.id": "first-github-agent-session",
            "user.id": "yuval.reuveni@checkmarx.com"
        },
    )
    result = agent("analyze the repository and create readme file ")
    print("Agent Result:", result)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())