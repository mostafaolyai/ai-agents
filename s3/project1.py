#assume we want to use add function in response, for that we need to create schema

import json
from dotenv import find_dotenv, load_dotenv 
from litellm import completion

load_dotenv(find_dotenv())


def celsius_to_fahrenheit(c: float) -> float:
    return (c * 9 / 5) + 32

AVAILABLE_FUNCTIONS = {"celsius_to_fahrenheit": celsius_to_fahrenheit}

convert_tool_schema = {
    "type": "function",
    "function": {
        "name": "celsius_to_fahrenheit",
        "description": "Convert celsius to fahrenheit",
        "parameters": {
            "type": "object",
            "properties": {
                "c": {"type": "number", "description": "celsius"},
            },
            "required": ["c"],
        },
    },
}



messages = [{"role": "user", "content": "convert 21 celsius to fahrenheit."}]


response = completion(
    model="gemini/gemini-flash-lite-latest",
    messages=messages,
    tools=[convert_tool_schema],
    tool_choice="required", 
)

response_message = response.choices[0].message 
print("پاسخ اولیه مدل:", response_message)

messages.append(response_message)

if response_message.tool_calls:
  for tool_call in response_message.tool_calls:
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments)

    function_to_call = AVAILABLE_FUNCTIONS[function_name]
    tool_output = function_to_call(**function_args)

    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "name": function_name,
        "content": str(tool_output),
    })

final_response = completion(
    model="gemini/gemini-flash-lite-latest",
    messages=messages,
)

print("پاسخ نهایی مدل به کاربر:")
print(final_response.choices[0].message.content)
