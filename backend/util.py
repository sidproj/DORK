import json


def serialize_tool_calls(tool_calls):

    return json.dumps([
        {
            "name": tool_call.function.name,
            "arguments": tool_call.function.arguments
        }
        for tool_call in tool_calls
    ])