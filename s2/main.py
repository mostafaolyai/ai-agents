from dotenv import find_dotenv, load_dotenv 
from litellm import completion

load_dotenv(find_dotenv())

# فراخوانی مدل Gemini
response = completion(model="gemini/gemini-flash-lite-latest", messages=[{"role": "user", "content": "Hello!"}])
    print(response.choices[0].message.content)

# فراخوانی مدل Anthropic با همان امضا و ساختار 
# response = completion( model="anthropic/claude-sonnet-4-5", messages=[{"role": "user", "content": "Hello!"}] )
# print(response)