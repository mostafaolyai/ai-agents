
import json
from dotenv import find_dotenv, load_dotenv
from litellm import completion

load_dotenv(find_dotenv())


# 1. Define Python functions

def add(a: int, b: int) -> int:
    return a + b


def multiply(a: int, b: int) -> int:
    return a * b


# 2. Map function names to Python functions

AVAILABLE_FUNCTIONS = {
    "add": add,
    "multiply": multiply
}


# 3. Define tool schemas

add_tool_schema = {
    "type": "function",
    "function": {
        "name": "add",
        "description": "Calculates the sum of two integers.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "integer",
                    "description": "The first number"
                },
                "b": {
                    "type": "integer",
                    "description": "The second number"
                }
            },
            "required": ["a", "b"]
        }
    }
}


multiply_tool_schema = {
    "type": "function",
    "function": {
        "name": "multiply",
        "description": "Multiplies two integers.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "integer",
                    "description": "The first number"
                },
                "b": {
                    "type": "integer",
                    "description": "The second number"
                }
            },
            "required": ["a", "b"]
        }
    }
}


# 4. Put all tools in a list

tools = [
    add_tool_schema,
    multiply_tool_schema
]


# 5. Initial user message

messages = [
    {
        "role": "user",
        "content": "What is 3 * (12 + 8)?"
    }
]


# 6. First call to the model

response = completion(
    model="gemini/gemini-flash-lite-latest",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)


response_message = response.choices[0].message

print("Initial model response:", response_message)


# 7. Tool calling loop

messages.append(response_message)

while response_message.tool_calls:

    for tool_call in response_message.tool_calls:

        function_name = tool_call.function.name

        function_args = json.loads(
            tool_call.function.arguments
        )

        print(f"\nCalling function: {function_name}")
        print(f"Arguments: {function_args}")

        # Find and execute the requested function
        function_to_call = AVAILABLE_FUNCTIONS[function_name]

        tool_output = function_to_call(**function_args)

        print(f"Tool output: {tool_output}")

        # Append tool result to conversation history
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": function_name,
            "content": str(tool_output)
        })

    # 8. Call model again with updated conversation

    response = completion(
        model="gemini/gemini-flash-lite-latest",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    response_message = response.choices[0].message

    messages.append(response_message)


# 9. Print final answer

print("\nFinal response:")
print(response_message.content)
