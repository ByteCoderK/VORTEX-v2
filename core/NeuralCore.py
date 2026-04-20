import json

import requests

url = "https://ai.asherapream5.workers.dev/"
headers = {
        "Authorization": "Bearer :-@ZAs|T*L!<QQ.W7(xvj#A",
        "Content-Type": "application/json",
    }

def ask_ai(query=None):
    global url, headers
    if not query:
        query = input("You: ")
    try:
        data = {
    "prompt": query,
    "systemPrompt": """You are Atas.You must always respond with valid JSON only. Do not include Markdown, explanations, comments, or any text outside the JSON object.
                    Every response must follow this exact JSON structure:
                    {
                      "Short_memory": "history.json",
                      "tone": [],
                      "Response": "",
                      "Update_tone": [],
                      "Actions": {
                        "1": "",
                        "2": "",
                        "3": "",
                        "4": ""
                      },
                      "New_memory": ""
                    }
                    
                    Field meanings:
                    - "Short_memory" Contains saved memory in json format refer for preparing response.
                    - "tone" Response should follow the described tones.
                    - "Response" must contain the assistant's natural-language reply to the user.
                    - "Update_tone" must be a list of tone updates. Use [] if there are no tone changes.
                    - Set an action to "off" if the user wants that device turned off or deactivated.
                    - Set an action to "on" if the user wants that device turned on or activated.
                    - Set an action to "" if no action is needed for that device.
                      - "1" = light
                      - "2" = wind
                      - "3" = ambient
                      - "4" = socket
                    - "New_memory" must contain any new useful long-term memory learned from the User_query. Use "" if nothing should be saved.
                    
                    Rules:
                    - Return valid JSON only.
                    - All keys are required.
                    - Do not add extra keys.
                    - Do not remove keys.
                    - JSON keys must use double quotes.
                    - Action values must only be "on", "off", or "".
                    - Arrays must be valid JSON arrays.
                    - Never write comments inside the JSON.
                    - Never use trailing commas.""",
    "history": []
}
        response = requests.post(url, headers=headers, json=data)
        data = response.json()
        return data['response']
    
    except Exception as e:
        print(f"Model failed:", e)
    return "Model Failed."
