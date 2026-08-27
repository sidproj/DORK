import os

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
# MODEL_NAME = os.getenv("MODEL_NAME", "qwen3:14b")
MODEL_NAME = os.getenv("MODEL_NAME", "qwen3:14b")
SYSTEM_PROMPT = "prompts/system.txt"
MAX_HISTORY = 20
TEMPERATURE = 0.7