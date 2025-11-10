from strands import Agent, tool
from ..config_base_model import get_base_model

# Define a specialized system prompt
SUMMARIZER_ASSISTANT_PROMPT = """
You are a specialized summarizer assistant that gets file content and produces concise summaries.
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
        summarizer_agent = Agent(
            system_prompt=SUMMARIZER_ASSISTANT_PROMPT,
            base_model=get_base_model()
        )

        # Call the agent and return its response
        response = summarizer_agent(query)
        return str(response)
    except Exception as e:
        return f"Error in summarizer assistant: {str(e)}"