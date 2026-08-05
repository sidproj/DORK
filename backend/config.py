import os

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "gemma4")
SYSTEM_PROMPT = "prompts/system.txt"
MAX_HISTORY = 20
TEMPERATURE = 0.7