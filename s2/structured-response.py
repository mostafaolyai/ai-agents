from litellm import completion 
from pydantic import BaseModel 

# تعریف ساختار مورد نظر به وسیله یک کلاس Pydantic 
class ExtractedInfo(BaseModel): 
    name: str 
    email: str 
    phone: str | None = None 
    
# ارسال درخواست به همراه فرمت خروجی مورد انتظار 
response = completion( model="gemini/gemini-flash-lite-latest", messages=[{ 
    "role": "user",
     "content": ( 
        "My name is John Smith, my email is john@example.com, and my phone"
        " is 555-1234."
        ), 
       }], 
       response_format=ExtractedInfo, 
       # اجبار مدل به تولید داده بر اساس این کلاس 
       ) 

result = response.choices[0].message.content 
print(result)