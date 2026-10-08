import os

from dotenv import load_dotenv
from strands import Agent
from strands.models.litellm import LiteLLMModel

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY", "")
if not api_key or "your-key-here" in api_key:
    raise SystemExit("OPENROUTER_API_KEY is missing or still a placeholder in .env")

model = LiteLLMModel(
    client_args={
        "api_key": api_key,
        "api_base": "https://openrouter.ai/api/v1",
    },
    model_id=os.getenv("MODEL_ID", "openrouter/openrouter/free"),
    params={"max_tokens": 2048},
)

agent = Agent(model=model)

result = agent("Say hello and tell me what model you are, in one sentence.")
print(result)
