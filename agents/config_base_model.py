
from strands.models.openai import OpenAIModel
import os
from dotenv import load_dotenv
from langfuse import observe, get_client as get_langfuse_client


def get_base_model(model_id: str="bedrock/eu.amazon.nova-pro-v1:0", stream: bool = True, x_request_id: str = "demo-request-strands-123", x_feature: str = "yuval-demo-strands", max_tokens: int = 1000, temperature: float = 0.7) -> OpenAIModel:
    load_dotenv()

    api_key=os.getenv("AIPROXY_API_KEY")
    if not api_key:
        raise ValueError("AIPROXY_API_KEY environment variable is required")
    stream = "/stream"
    model = OpenAIModel(
    client_args={
                    "api_key": api_key,
                    "base_url": f"https://ast-master-components.dev.cxast.net/api/ai-proxy-py/litellm{stream}",
                    "default_headers": {
                        "X-Request-ID": x_request_id,
                        "X-Feature": x_feature,
                    },
                },
        model_id=model_id,
        params={
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
    )
    return model