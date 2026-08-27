from prompts.identity import IDENTITY
from prompts.rules import RULES
from prompts.tools import TOOL_RULES
from prompts.runtime import runtime

class PromptManager:

    @staticmethod
    def build(messages):

        prompt = []

        prompt.append({
            "role":"system",
            "content":IDENTITY
        })

        prompt.append({
            "role":"system",
            "content":RULES
        })
        
        prompt.append({
            "role":"system",
            "content":TOOL_RULES
        })

        prompt.append({
            "role":"system",
            "content":runtime()
        })

        prompt.extend(messages[:-1])

        prompt.append({
            "role":"system",
            "content":"The next user message is the user's CURRENT request. Answer it."
        })

        prompt.append(messages[-1])

        return prompt