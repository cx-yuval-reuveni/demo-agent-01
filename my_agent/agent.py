from strands import Agent
from strands.models.openai import OpenAIModel
from strands.models import BedrockModel
from strands_tools import  calculator
import os
from dotenv import load_dotenv
load_dotenv()

apii_key=os.getenv("AIPROXY_API_KEY")

model = OpenAIModel(
client_args={
                "api_key": "",
                "base_url": "https://ast-master-components.dev.cxast.net/api/ai-proxy-py/litellm/stream",
                "default_headers": {
                    "Authorization": f"Bearer {apii_key}",
                    "X-Request-ID": "demo-request-strands-123",
                    "X-Feature": "yuval-demo-strands",
                },
            },
    # **model_config
    model_id="bedrock/eu.anthropic.claude-3-7-sonnet-20250219-v1:0",
    params={
        "max_tokens": 1000,
        "temperature": 0.7,
    }
)
agent = Agent(model=model, tools=[calculator])
response = agent("What is 2+2")
print(response)