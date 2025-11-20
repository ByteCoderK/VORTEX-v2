import os
import sys
import json
import threading
from openai import OpenAI
project_root = os.path.abspath("C:\\Users\\User One\\Desktop\\VORTEX-v2")
sys.path.append(project_root)
from commands.NeuralCore import*


MemoryCACHE = []
keys = {
    'KEY_1': 'sk-or-v1-4e12e8608cbcc3a4eb873e 6d04fbf8a58d53d873d7a968195b2caae7aa3c25bd',
    'KEY_2': "sk-or-v1-3df21746fdcbe043d2eefe 54abc3c3cf5afa4568393cb6da7810cfb492d213a1",
    'KEY_3': 'sk-or-v1-0ad6a492cedc75a7518ccc 86b5d8806b77004765255429a13f13477ea41cc2f0',
    'KEY_4': 'sk-or-v1-797084af041ee7149e1d64 833163a48ba809826151ce8562db9d027f263f876b'
}
def rememberMeProtocol(query,CURRENT_key=keys["KEY_1"]):
    try:
    model_keys = list(keys.values())
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=CURRENT_key
)
    
        completion = client.chat.completions.create(
            model='kwaipilot/kat-coder-pro:free',
            messages=[
                {
                    "role": "system",
                    "content": """Respond ONLY with pure JSON. Example outputs:
{"user_name": "John"} for names
{"country": "France"} for locations
{"preferences": ["pizza"]} for likes
{"reminders": ["Call mom"]} for tasks
    {"friends_name": ["sonu","arun"]} for names
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
        response_data = json.loads(response_text)    # Extract JSON data
        return "MEMORY EXTRACTED" + response_text  # Print the JSON data for debugging
    except Exception as e:
        # Fallback logic: try next model
        current_index = model_keys.index(CURRENT_key)
        if current_index + 1 < len(model_keys):
            next_model_key = model_keys[current_index + 1]
            return rememberMeProtocol(query, next_model_key)
        else:
            return "All models failed..."
