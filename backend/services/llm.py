import time
import ollama
from config import MODEL_NAME

class LLMService:

    @staticmethod
    def chat(messages,think=True):

        response = ollama.chat(
            model=MODEL_NAME,
            messages=messages,
            options={
                "temperature": 0.7,
            },
            think=think
        )

        message = response.message

        return {
            "role": message.role,
            "content": message.content,
        }