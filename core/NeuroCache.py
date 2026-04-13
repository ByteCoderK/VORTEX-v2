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
    "KEY_1": "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",
    "KEY_2": "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",
    "KEY_3": "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",
    "KEY_4": "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"
}

# Create a clean ordered list so Python doesn't screw you
model_keys = [keys[k] for k in sorted(keys.keys())]

def write_memory(memory_list):
    with open("memory.txt", "a", encoding="utf-8") as f:
        safe_list = [str(item) for item in memory_list if item is not None]
        f.write("\n".join(safe_list) + "\n")


def rememberMeProtocol(query, CURRENT_key=keys["KEY_1"]):

    if CURRENT_key not in model_keys:
        CURRENT_key = model_keys[0]

    for idx, key in enumerate(model_keys):

        if key != CURRENT_key:
            continue

        try:
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=key
            )

            completion = client.chat.completions.create(
                model='meta-llama/llama-3.3-70b-instruct:free',
                messages=[
                    {
                        "role": "system",
                        "content": (
                            'Respond ONLY in JSON. If nothing to store, return {}.'
                        )
                    },
                    {"role": "user", "content": query}
                ],
                extra_headers={
                    "X-Title": "VORTEX",
                    "HTTP-Referer": "http://localhost"
                }
            )

            response_text = completion.choices[0].message.content

            # Attempt JSON parsing
            try:
                memory_json = json.loads(response_text)
            except:
                memory_json = {}

            return memory_json

        except Exception as e:
            next_index = idx + 1
            if next_index < len(model_keys):
                CURRENT_key = model_keys[next_index]
                continue
            else:
                return {}