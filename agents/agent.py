from strands import Agent
from strands_tools import  calculator
import os
from .config_base_model import get_base_model


model = get_base_model(
    model_id="bedrock/claude-sonnet-3-7",
    stream=True,
    x_request_id="demo-request-strands-123",
    x_feature="yuval-demo-strands",
    max_tokens=1000,
    temperature=0.7)

agent = Agent(model=model, tools=[calculator])
response = agent("What is 2+2*3-4/2+1")
