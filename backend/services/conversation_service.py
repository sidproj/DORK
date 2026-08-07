from datetime import datetime
import json
import time

from repositories.conversation_repository import ConversationRepository
from repositories.message_repository import MessageRepository

from services.prompt_manager import PromptManager
from services.llm import LLMService
from services.title_service import TitleService
from services.sse_event import sse_event


class ConversationService:
    
    @staticmethod
    def get_messages(conversation_id: int):

        return MessageRepository.get_by_conversation(
            conversation_id
        )

    @staticmethod
    def create():

        return ConversationRepository.create()

    @staticmethod
    def chat(
        conversation_id: int | None,
        user_message: str
    ):
        if conversation_id is None:
            conversation_id = ConversationRepository.create()

        new_user_message = MessageRepository.create(
            conversation_id,
            "user",
            user_message
        )

        history = MessageRepository.get_by_conversation(conversation_id)

        messages = [
            {
                "role": message.role,
                "content": message.content
            }
            for message in history
        ]
        
        conversation = ConversationRepository.get(conversation_id)
        
        if(conversation.title.lower() == "new chat"):
            title = TitleService.generate_title(history)
            
            if title != TitleService.NO_TITLE:
                ConversationRepository.update_title(conversation_id,title)
                conversation.title = title

        prompt = PromptManager.build(messages)
        
        assistant = LLMService.chat(prompt)
        
        assistant_message = MessageRepository.create(
            conversation_id,
            assistant['role'],
            assistant['content']
        )

        return {
            "conversation": conversation,
            "messages": [new_user_message,assistant_message]
        }
    
    @staticmethod
    def stream_chat(
        conversation_id: int | None,
        user_message: str
    ):
        
        # TODO:
        # 1. Save user message
        # 2. Generate title
        # 3. Build prompt
        conversation = None
        if conversation_id is None:
            conversation = ConversationRepository.create()
            conversation_id = conversation.id
        MessageRepository.create(
            conversation_id,
            "user",
            user_message
        )

        history = MessageRepository.get_by_conversation(conversation_id)

        messages = [
            {
                "role": message.role,
                "content": message.content
            }
            for message in history
        ]
        
        conversation = ConversationRepository.get(conversation_id)
        
        if(conversation.title.lower() == "new chat"):
            title = TitleService.generate_title(history)
            
            if title != TitleService.NO_TITLE:
                ConversationRepository.update_title(conversation_id,title)
                conversation.title = title
                
        prompt = PromptManager.build(messages)
        
        yield {
            "type":"start",
            "content":{}
        }
        
        assistant_response = ""
        
        for token in LLMService.stream_chat(prompt):

            assistant_response += token

            yield {
                "type": "token",    
                "content": token,
            }
        
        MessageRepository.create(
            conversation_id,
            "assistant",
            assistant_response
        )
        yield {
            "type":"done",
            "content":assistant_response
        }