import asyncio 
from litellm import acompletion 

# تعریف یک تابع ناهمگام (Coroutine)  
async def get_response(prompt: str) -> str: 
    response = await acompletion( model="gemini/gemini-flash-lite-latest", messages=[{"role": "user", "content": prompt}] ) 
    return response.choices[0].message.content 
    
prompts = [ 
    "What is 2 + 2?", 
    "What is the capital of Japan?", 
    "Who wrote Romeo and Juliet?", 
    ] 
    

async def main(): 
    # ساخت تسک‌ها برای هر پرامپت 
    tasks = [get_response(p) for p in prompts] 
    # اجرای همزمان همه درخواست‌ها 
    results = await asyncio.gather(*tasks) 
    
    for prompt, result in zip(prompts, results): 
        print(f"Q: {prompt}") 
        print(f"A: {result}\\n") 
    # اجرای حلقه رویداد 


asyncio.run(main())