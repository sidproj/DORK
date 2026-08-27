import ollama
from config import MODEL_NAME

class LLMService:

    @staticmethod
    def chat(messages,tools=None,think=True):
        
        response = ollama.chat(
            model=MODEL_NAME,
            messages=messages,
            tools=tools,
            think=think,
            options={"temperature": 0.7},
        )
        
        message = response.message

        return {
            "role": message.role,
            "content": message.content,
            "tool_calls":message.tool_calls or []
        }

    @staticmethod
    def stream_chat(messages,tools=None,think=True):
        response = ollama.chat(
            model=MODEL_NAME,
            messages=messages,
            stream=True,
            tools=tools,
            think=think,
            options={"temperature": 0.7},
        )
        for chunk in response:
            message = chunk.message
            if message.content:
                yield {
                    "type":"token",
                    "content":message.content
                }

            if message.tool_calls:
                yield {
                    "type":"tool_calls",
                    "tool_calls":message.tool_calls
                }