from repositories.conversation_repository import ConversationRepository
from repositories.message_repository import MessageRepository

from services.prompt_manager import PromptManager
from services.agent_service import AgentService
from services.title_service import TitleService

from tools.resgistry import ToolRegistry
from tools.executor import ToolExecutor
from tools.calculator import CalculatorTool
from tools.datetime_tool import DateTimeTool
from tools.web_search import WebSearchTool
from tools.web_fetch import WebFetchTool

class ConversationService:
    
    tool_registry = ToolRegistry()
    tool_registry.register(CalculatorTool)
    tool_registry.register(DateTimeTool)
    tool_registry.register(WebSearchTool)
    tool_registry.register(WebFetchTool)
    tool_executor = ToolExecutor(tool_registry)
    agent_service = AgentService(tool_executor)

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
        
        agent_result = ConversationService.agent_service.run(prompt)

        assistant = agent_result["response"]
        generated_messages = agent_result["messages"]
        
        for message in generated_messages:
            MessageRepository.create(
                conversation_id,
                message["role"],
                message["content"],
                tool_calls=message.get("tool_calls")
            )
        
        assistant_message = MessageRepository.create(
            conversation_id,
            assistant['role'],
            assistant['content'],
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
        
        for event in ConversationService.agent_service.stream(prompt):
            event_type = event["type"]
            
            if event_type == "token":
                assistant_response += event["content"]
                yield event
            elif event_type == "assistant_tool_call":
                
                MessageRepository.create(
                    conversation_id,
                    "assistant",
                    event["content"],
                    tool_calls=event["tool_calls"]
                )

                yield event
            elif event_type == "tool_result":
                
                MessageRepository.create(
                    conversation_id,
                    "tool",
                    event["content"]
                )
                
                yield event
                
            elif event_type == "assistant_complete":
                assistant_response = event["content"]
            else:
                yield event
        
        assistant_message = MessageRepository.create(
            conversation_id,
            "assistant",
            assistant_response
        )
        
        yield {
            "type": "done",
            "content": assistant_response,
            "message_id": assistant_message.id
        }