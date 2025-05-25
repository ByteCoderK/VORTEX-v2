import os
import sys
import json
import threading
from openai import OpenAI
project_root = os.path.abspath("C:\\Users\\User One\\Desktop\\VORTEX-v2")
sys.path.append(project_root)
from commands.NeuralCore import *

MemoryCACHE = []
aiModels = {'ai_I' : 'meta-llama/llama-3.3-8b-instruct:free','ai_II' : "qwen/qwen3-32b:free",
           'ai_III' : "mistralai/devstral-small:free",'ai_IV' : "nousresearch/deephermes-3-mistral-24b-preview:free"}
model_key='ai_I'

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
)

def rememberMeProtocol(query, model_key):
    try:
        print(query)
        completion = client.chat.completions.create(
            model=aiModels[model_key],
            messages=[
                {
                    "role": "system",
                    "content": """Respond ONLY with pure JSON. Example outputs:
{"user_name": "John"} for names
{"country": "France"} for locations
{"preferences": ["pizza"]} for likes
{"reminders": ["Call mom"]} for tasks
{} for no data,SPEACIAL NOTE : NO OTHER RESPONSE NEEDED!! """

                },
                {
                    "role": "user",
                    "content": query
                }
            ],
            extra_headers={
                "X-Title": "VORTEX",
                "HTTP-Referer": "http://localhost"
            },
            extra_body={}
        )
        response_text = completion.choices[0].message.content
        print(f"Response Text: {response_text}")
        response_data = json.loads(response_text)
        print(f"Parsed JSON: {response_data}")
        if response_data:
            MemoryCACHE.append(response_data)
            print(f"MemoryCACHE: {MemoryCACHE}")
        else:
            print("MemoryCACHE: empty")
    except Exception as e:
        print(f"Error with model {model_key}: {e}")
        # Fallback logic: try next model
        model_keys = list(aiModels.keys())
        current_index = model_keys.index(model_key)
        if current_index + 1 < len(model_keys):
            next_model_key = model_keys[current_index + 1]
            print(f"Falling back to model: {next_model_key}")
            rememberMeProtocol(query, next_model_key)
        else:
            print("All models failed.")


query = 'hi my name is asher'    
t1= threading.Thread(target=ask_ai)
t2 = threading.Thread(target=rememberMeProtocol, args=(query,model_key))  
#t1.start()  
#t2.start()