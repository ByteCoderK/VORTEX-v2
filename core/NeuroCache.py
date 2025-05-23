import os
import sys
import json
import threading
from openai import OpenAI
project_root = os.path.abspath("C:\\Users\\User One\\Desktop\\VORTEX-v2")
sys.path.append(project_root)
from commands.NeuralCore import *

MemoryCACHE = []

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
)

def rememberMeProtocol(query: str) -> dict:
    print("rememberMeProtocol")
    try:
        completion = client.chat.completions.create(
            model="meta-llama/llama-3.3-8b-instruct:free",
            messages=[
                {
                    "role": "system",
                    "content": """Respond ONLY with pure JSON. Example outputs:
{"user_name": "John"} for names
{"country": "France"} for locations
{"preferences": ["pizza"]} for likes
{"reminders": ["Call mom"]} for tasks
{} for no data"""
                },
                {
                    "role": "user",
                    "content": query  # <- This is how you pass the user question
                }
                ],
            extra_headers={
                "X-Title": "VORTEX",
                "HTTP-Referer": "http://localhost"  # Optional
                },
            extra_body={}
            )
        
        # Get the raw response content
        response_text = completion.choices[0].message.content
        print(f"Response Text: {response_text}")
        # Parse the JSON response
        response_data = json.loads(response_text)
        print(f"Parsed JSON: {response_data}")
        
        # Store in memory if not empty
        if response_data:
            MemoryCACHE.append(response_data)
            print("fi else loop")
            print(f"MemoryCACHE: {MemoryCACHE}")
        else:
            print("MemoryCACHE: empty")
    except json.JSONDecodeError:
        print("Received invalid JSON response")
        return 'eeeeeeeeeeeeeeeeeeeeeeeeee'
    except Exception as e:
        print(f"Error: {e}")
        return '-----------------'
    
t1= threading.Thread(target=ask_ai)
t2 = threading.Thread(target=rememberMeProtocol, args=(query,))  
query = 'hi my name is asher'
#t1.start()  
t2.start()