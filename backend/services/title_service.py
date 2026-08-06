import json

from ollama import Message

from services.llm import LLMService
from prompts.title import TITLE_SYSTEM_PROMPT

class TitleService:
    
    NO_TITLE = "NO_TITLE"
    MAX_CONTEXT_MESSAGES = 8
    GREETING_MESSAGES = {
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening",
        "thanks",
        "thank you",
        "ok",
        "okay",
        "sure",
        "bye",
        "goodbye",
        "yo",
        "sup",
        "hola",
    }
    
    @staticmethod
    def generate_title(messages:list[Message])-> str:
        
        try:
            if not TitleService._should_generate_title(messages):
                return TitleService.NO_TITLE
            prompt = TitleService._build_prompt(messages)
            response = LLMService.chat(prompt)
            title = response.get("content")
            return title if title else TitleService.NO_TITLE
        except Exception as e:
            print("Exception generate title: ",e)
            return TitleService.NO_TITLE
    
    @staticmethod
    def _should_generate_title(messages: list[Message]) -> bool:
        try:
            user_messages = [
                message.content.strip()
                for message in messages
                if message.role == "user"
            ]

            if not user_messages:
                return False
            
            for message in user_messages:
                normalized = " ".join(message.lower().split())

                if normalized in TitleService.GREETING_MESSAGES:
                    continue

                if len(normalized) < 10:
                    continue

                return True
            return False
        except Exception as e:
            print("Exception should generate: ",e)
            return False
    
    @staticmethod
    def _build_prompt(messages:list[Message])->list[dict]:
        # improve upon later to remove the common greeting messages to not send it in LLM
        user_messages = [m.content for m in messages if m.role == "user"]
        prompt = [
            {
                "role": "system",
                "content": TITLE_SYSTEM_PROMPT+ 
                "|".join(user_messages),
            }
        ]
        
        return prompt