import json

from services.llm import LLMService

class AgentService:
    MAC_ITERATIONS = 10
    
    def __init__(self,tool_executor):
        self.tool_executor = tool_executor
    
    @staticmethod
    def serialize_tool_calls(tool_calls):
        return [
            {
                "name": tool_call.function.name,
                "arguments": tool_call.function.arguments
            }
            for tool_call in tool_calls
        ]
    
    def run(self,messages):
        
        current_messages = list(messages)
        generated_messages = []
        
        for _ in range(self.MAC_ITERATIONS):
            
            response = LLMService.chat(
                messages=current_messages,
                tools= self.tool_executor.registry.get_definitions(),
                think=False
            )
            
            tool_calls = response.get("tool_calls")
            
            # LLM produced a normal response
            if not tool_calls:
                return {
                    "response": response,
                    "messages": generated_messages
                }
            
            assistant_message = {
                "role": "assistant",
                "content": response.get("content", ""),
                "tool_calls": tool_calls
            }
            
            db_assistant_message = {
                "role": "assistant",
                "content": response.get("content", ""),
                "tool_calls": json.dumps(AgentService.serialize_tool_calls(tool_calls))
            }


            current_messages.append(assistant_message)
            generated_messages.append(db_assistant_message)
            
            for tool_call in response.get("tool_calls"):
                tool_name = tool_call.function.name
                arguments = tool_call.function.arguments
                
                result = self.tool_executor.execute(
                    tool_name,
                    arguments
                )
                print("Tool result: ",result)
                
                tool_content = None
                
                if result["success"]:
                    tool_content = str(result["result"])
                else:
                    tool_content = result["error"]

                tool_message = {
                    "role": "tool",
                    "content": tool_content
                }

                current_messages.append(tool_message)
                generated_messages.append(tool_message)
        raise RuntimeError("Agent exceeded maximum tool iterations.")
    
    def stream(self,messages):
        
        current_messages = list(messages)
        
        for _ in range(self.MAC_ITERATIONS):
            tool_calls = None
            assistant_content = ""
            
            for event in LLMService.stream_chat(
                messages=current_messages,
                tools=self.tool_executor.registry.get_definitions(),
                think=False
            ):
                if event["type"] == "token":
                    assistant_content += event['content']
                    yield event
                
                elif event["type"] == "tool_calls":
                    tool_calls = event["tool_calls"]
            
            if not tool_calls:
                yield {
                    "type": "assistant_complete",
                    "content": assistant_content
                }

                return
            
            assistant_message = {
                "role":"assistant",
                "content":assistant_content,
                "tool_calls":tool_calls
            }
            
            current_messages.append(assistant_message)
            
            yield {
                "type": "assistant_tool_call",
                "content": assistant_content,
                "tool_calls": json.dumps(AgentService.serialize_tool_calls(tool_calls))
            }
            
            for tool_call in tool_calls:
                tool_name = tool_call.function.name
                arguments = tool_call.function.arguments
                
                yield {
                    "type":"tool_call",
                    "tool":tool_name,
                    "arguments":arguments
                }
                
                result = self.tool_executor.execute(tool_name,arguments)
                
                print("Tool result:",result)
                
                if result["success"]:
                    tool_content = str(result["result"])
                else:
                    tool_content = str(result["error"])

                tool_message = {
                    "role":"tool",
                    "content":tool_content
                }
                
                current_messages.append(tool_message)
            
            yield {
                "type": "tool_result",
                "tool": tool_name,
                "content": tool_content,
                "success": result["success"]
            }
        
        raise RuntimeError(
            "Agent exceeded maximum tool iterations."
        )
                
    def _get_tool_definitions(self):
        return self.tool_executor.registry.get_definitions()