from litellm import completion 
from pydantic import BaseModel 

# تعریف ساختار مورد نظر به وسیله یک کلاس Pydantic 
class BookSummary(BaseModel): 
    title: str 
    year: int 
    key_takeaways: list[str]
    
# ارسال درخواست به همراه فرمت خروجی مورد انتظار 
response = completion( model="gemini/gemini-flash-lite-latest", messages=[{ 
    "role": "user",
     "content": ( 
        "Give me summary of 'Who Moved My Cheese?'"
        ), 
       }], 
       response_format=BookSummary, 
       # اجبار مدل به تولید داده بر اساس این کلاس 
       ) 

result = response.choices[0].message.content 
print(result)