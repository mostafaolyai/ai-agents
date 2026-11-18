from litellm import completion
# درخواست اول 
response1 = completion( model="gemini/gemini-flash-lite-latest", messages=[{"role": "user", "content": "My name is Mosi."}], ) 
print(response1.choices[0].message.content) 
# درخواست دوم 
response2 = completion( model="gemini/gemini-flash-lite-latest", messages=[{"role": "user", "content": "What is my name?"}] ) 
print(response2.choices[0].message.content)