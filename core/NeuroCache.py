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
    'KEY_4': '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'
}

# Create a clean ordered list so Python doesn't screw you
model_keys = [keys[k] for k in sorted(keys.keys())]

def write_memory(memory_dict):
    if not memory_dict:
        return  # nothing to save

    with open("memory.txt", "a", encoding="utf-8") as f:
        f.write(json.dumps(memory_dict, ensure_ascii=False) + "\n")


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
                model='kwaipilot/kat-coder-pro:free',
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