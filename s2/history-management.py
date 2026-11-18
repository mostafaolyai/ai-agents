from litellm import completion 

messages = [] 

# تبادل اول 
messages.append({"role": "user", "content": "My name is Mosi."}) 
response1 = completion(model="gemini/gemini-flash-lite-latest", messages=messages) 
assistant_message1 = response1.choices[0].message.content 

# افزودن پاسخ مدل به تاریخچه 
messages.append({"role": "assistant", "content": assistant_message1}) 
print(assistant_message1) 

# تبادل دوم - ارسال تمام تاریخچه شامل پیام‌های قبلی 
messages.append({"role": "user", "content": "What is my name?"}) 
response2 = completion(model="gemini/gemini-flash-lite-latest", messages=messages) 
assistant_message2 = response2.choices[0].message.content 
print(assistant_message2)