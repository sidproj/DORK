import ollama
from config import MODEL_NAME

class LLMService:

    @staticmethod
    def chat(messages):
        response = ollama.chat(
            model=MODEL_NAME,
            messages=messages,
            think=True,
            options={"temperature": 0.7},
        )
        message = response.message
        return {
            "role": message.role,
            "content": message.content,
        }

    @staticmethod
    def stream_chat(messages):
        response = ollama.chat(
            model=MODEL_NAME,
            messages=messages,
            stream=True,
            think=True,
            options={"temperature": 0.7},
        )
        for chunk in response:
            content = chunk.message.content
            if content:
                yield content