from strands import Agent
from strands.models import BedrockModel
from strands_tools import calculator
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Use the BedrockModel directly instead of the OpenAI wrapper
# Claude 3 Haiku is a Bedrock model, so we should use BedrockModel
model = BedrockModel(
    client_args={
        "aws_region": os.getenv("AWS_REGION", "eu-west-1"),
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
    },
    # model ID for Claude 3 Haiku on Bedrock
    model_id="eu.anthropic.claude-3-haiku-20240307-v1:0",
    params={
        "max_tokens": 1000,
        "temperature": 0.7,
    }
)

# Initialize the agent with the model and calculator tool
agent = Agent(model=model, tools=[calculator])

# Test the agent
try:
    response = agent("What is 2+2")
    print(response)
except Exception as e:
    print(f"Error: {e}")
    print(f"Error type: {type(e)}")