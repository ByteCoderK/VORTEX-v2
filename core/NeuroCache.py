import os
import sys
import json
import threading
from openai import OpenAI
project_root = os.path.abspath("C:\\Users\\User One\\Desktop\\VORTEX-v2")
sys.path.append(project_root)
from commands.NeuralCore import *

MemoryCACHE = []
keys = {
    'KEY_1': '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',
    'KEY_2': "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",
    'KEY_3': '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',
}
CURRENT_key=keys["KEY_1"]
def rememberMeProtocol(query,CURRENT_key):
    model_keys = list(keys.values())
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=CURRENT_key
)
    try:
        completion = client.chat.completions.create(
            model='meta-llama/llama-3.3-8b-instruct:free',
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
        response_data = json.loads(response_text)    # Extract JSON data
        return f"Parsed JSON: {response_data}"
    except Exception as e:
        # Fallback logic: try next model
        current_index = model_keys.index(CURRENT_key)
        if current_index + 1 < len(model_keys):
            next_model_key = model_keys[current_index + 1]
            rememberMeProtocol(query, next_model_key)
        else:
            return "All models failed."