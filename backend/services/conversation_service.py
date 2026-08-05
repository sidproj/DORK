from repositories.conversation_repository import ConversationRepository
from repositories.message_repository import MessageRepository

from services.prompt_manager import PromptManager
from services.llm import LLMService


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

        history = MessageRepository.get_by_conversation(
            conversation_id
        )

        messages = [
            {
                "role": message.role,
                "content": message.content
            }
            for message in history
        ]

        prompt = PromptManager.build(messages)

        assistant = LLMService.chat(prompt)
        
        assistant_message = MessageRepository.create(
            conversation_id,
            assistant["role"],
            assistant["content"]
        )

        return {
            "conversation_id": conversation_id,
            "messages": [new_user_message,assistant_message]
        }