from strands import Agent, tool
from agents.config_base_model import get_base_model  # absolute import for package execution

# Define a specialized system prompt
SUMMARIZER_ASSISTANT_PROMPT = """
You are a specialized summarizer assistant that gets file content and produces concise summaries.
you have access to github mcp server to retrieve file contents from GitHub repositories.
When given a user query, generate a concise summary of the provided content.
"""

@tool
def summarizer_assistant(query: str) -> str:
    """
    Process and respond to summarization-related queries.

    Args:
        query: str: The input query requiring summarization.

    Returns:    
        A concise summary of the provided content
    """
    try:
        # Strands Agents SDK makes it easy to create a specialized agent
        model = get_base_model()
        summarizer_agent = Agent(
            system_prompt=SUMMARIZER_ASSISTANT_PROMPT,
            model=model,
            tools=[],
        )

        # Call the agent and return its response
        response = summarizer_agent(query)
        return str(response)
    except Exception as e:
        return f"Error in summarizer assistant: {str(e)}"