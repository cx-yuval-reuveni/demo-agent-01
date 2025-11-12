import os
from strands import Agent
from agents.swarm.summarizer import summarizer_assistant  # absolute import
from agents.config_base_model import get_base_model  # absolute import
from mcp import StdioServerParameters, stdio_client
from strands.tools.mcp import MCPClient
import numpy as np
import base64
from dotenv import load_dotenv
load_dotenv()
# add langfuse telemetry if env vars are set


MAIN_SYSTEM_PROMPT = """
You are a planner agent that delegates tasks to specialized assistants.
You have access to github mcp_tool to extract the folder structure from GitHub repositories.
you should only extract the file structure of a repo."""


#"your job is to extract the file structure from the repo and identify files that need to be summarized."
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


    model = get_base_model()
    github_mcp_client = MCPClient(lambda: stdio_client(github_server_params()))
    with github_mcp_client:
        tools = github_mcp_client.list_tools_sync() + [summarizer_assistant]
        # Safely introspect MCPAgentTool wrapper objects
        for tool in tools:
            name = getattr(tool, "tool_name", getattr(tool, "name", type(tool).__name__))
            description = ""
            underlying = getattr(tool, "mcp_tool", None)
            if underlying is not None and hasattr(underlying, "description"):
                description = underlying.description or ""
            elif hasattr(tool, "description"):
                description = getattr(tool, "description") or ""
            print(f"Loaded tool: {name} - {description}")

        repo_path = "cx-yuval-reuveni/demo-agent-01"
        repo_name = repo_path.split("/")[-1]
        planner_agent = Agent(
            system_prompt=MAIN_SYSTEM_PROMPT,
            tools=tools,
            model=model,
            trace_attributes={
                "session.id": f"multiagent-mock-{random_session}",
                "user.id": "yuval.reuveni@checkmarx.com",
                "repo.name": repo_name,
            },
        )
        try:
            result = planner_agent(
                f"Read the repo structure without reading the content of the files: https://github.com/{repo_path} and create a graph of the file structure. add the files that are inside the folders as well."
            )
        except Exception as e:
            print(f"[error] agent invocation failed: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 