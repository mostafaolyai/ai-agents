#assume we want to use add function in response, for that we need to create schema

import json
from dotenv import find_dotenv, load_dotenv 
from litellm import completion

load_dotenv(find_dotenv())


def add(a: int, b: int) -> int:
  """جمع دو عدد صحیح"""
  return a + b

# دیکشنری نگاشت نام تابع به شیء تابع در پایتون 
AVAILABLE_FUNCTIONS = {"add": add}

add_tool_schema = {
    "type": "function",
    "function": {
        "name": "add",
        "description": "Calculates the sum of two integers.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "integer", "description": "The first number"},
                "b": {"type": "integer", "description": "The second number"},
            },
            "required": ["a", "b"],
        },
    },
}


# ۲. پیام اولیه کاربر
messages = [{"role": "user", "content": "What is 42 plus 58?"}]

# ۳. ارسال درخواست به همراه لیست ابزارها (tools)
response = completion(
    model="gemini/gemini-flash-lite-latest",
    messages=messages,
    tools=[add_tool_schema],
    tool_choice="auto",  # خود مدل تصمیم بگیرد که نیاز به ابزار دارد یا خیر
)

response_message = response.choices[0].message 
print("پاسخ اولیه مدل:", response_message)

# maybe it doesnt return response, so we need to check if the model wants to use the tool

# الف) اضافه کردن پیام حاوی درخواست ابزار به تاریخچه
messages.append(response_message)

# ب) پیمایش درخواست‌های ابزار (مدل می‌تواند همزمان چند ابزار بخواهد)
if response_message.tool_calls:
  for tool_call in response_message.tool_calls:
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments)

    # پیدا کردن تابع در دیکشنری و اجرای آن با ورودی‌های استخراج‌شده
    function_to_call = AVAILABLE_FUNCTIONS[function_name]
    tool_output = function_to_call(**function_args)

    # ج) ثبت نتیجه ابزار در قالب پیام جدید با role: tool
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,  # اتصال خروجی به درخواست متناظر
        "name": function_name,
        "content": str(tool_output),
    })

# د) فراخوانی مجدد مدل با تاریخچه کامل برای دریافت پاسخ نهایی
final_response = completion(
    model="gemini/gemini-flash-lite-latest",
    messages=messages,
)

print("پاسخ نهایی مدل به کاربر:")
print(final_response.choices[0].message.content)
