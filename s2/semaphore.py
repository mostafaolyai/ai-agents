# When you send many requests simultaneously, two problems arise: rate limits from the API provider and transient failures from network problems or server overload. LiteLLM’s `num_retries` parameter handles transient failures with automatic exponen- tial backoff. For rate limiting, you can use Python’s `asyncio.Semaphore` to limit how many requests run concurrently.

# The key insight is that `Semaphore` controls access at the `async` `with` block level. By wrapping the `acompletion` call itself, we ensure that no matter how many tasks are run- ning, the number of actual API calls that can happen at the same time is limited.

import asyncio 
from dotenv import find_dotenv, load_dotenv
from litellm import acompletion 

load_dotenv(find_dotenv())

# محدود کردن به حداکثر ۱۰ درخواست همزمان در هر لحظه 
semaphore = asyncio.Semaphore(2)

async def call_llm(prompt: str) -> str: 
    """فراخوانی مدل با کنترل نرخ و تلاش مجدد خودکار""" 
    async with semaphore: # ورود به بخش کنترل‌شده 
        response = await acompletion( 
            model="gemini/gemini-flash-lite-latest", 
            messages=[{"role": "user", "content": prompt}], 
            num_retries=3, # در صورت قطعی یا خطای موقت، تا ۳ بار دوباره تلاش کن 
        ) 
        # print('---',  response.choices[0].message.content)
        return response.choices[0].message.content

async def run_batch(): 
    prompts = [f"What is {i} + {i}?" for i in range(10)] 
    tasks = [call_llm(p) for p in prompts] 
    # return_exceptions=True مانع کرش کردن برنامه در صورت خطای یک درخواست می‌شود 
    results = await asyncio.gather(*tasks) 
    print(f"تعداد کل خروجی‌های دریافت شده: {len(results)}") 

asyncio.run(run_batch())