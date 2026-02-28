import ollama
from flask import current_app

class LLMService:
    
    @staticmethod
    def generate_response(messages:list[str]):
        model = current_app.config['MODEL_NAME']
        
        stream = ollama.chat(
            model=model,
            messages=messages,
            stream=True
        )
        
        for chunk in stream :
            content = chunk['message']['content']
            if content:
                yield content