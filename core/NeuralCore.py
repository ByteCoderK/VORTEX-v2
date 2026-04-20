import json
import requests

url = "https://ai.asherapream5.workers.dev/"
headers = {
        "Authorization": "Bearer :-@ZAs|T*L!<QQ.W7(xvj#A",
        "Content-Type": "application/json",
    }

def load_history():
    try:
        with open("history.json", "r", encoding="utf-8") as history_file:
            history = json.load(history_file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

    if not isinstance(history, list):
        return []
    clean_history = []

    for message in history:
        if not isinstance(message, dict):
            continue

        role = message.get("role")
        content = message.get("content")

        if role not in ["user", "assistant"]:
            continue

        if not isinstance(content, str):
            continue

        clean_history.append({
            "role": role,
            "content": content
        })
    return clean_history
    
def save_history(history):
    with open('history.json','w',encoding='utf-8') as history_file:
        json.dump(history, history_file,indent=4)

history = load_history()
def ask_ai(query=None):
    global url, headers,history
    if not query:
        query = input("You: ")
    try:
        data = {
    "prompt": query,
    "systemPrompt": """You are Atas.You must always respond with valid JSON only in the given format.Do not include Markdown, explanations, comments, or any text outside the JSON object.
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
                    - "Response" field contains the Ai's reply to the prompt.
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
    "history": history
}
        output = requests.post(url, headers=headers, json=data)
        response = output.json()
        try:
            json_data = json.dumps(response['response'], indent=4)
        except Exception as error:
            print("Error parsing JSON:", error)
            return "Error parsing JSON:", error
        data = json.loads(json_data)
        history = load_history()
        history.append({
                        "role": "user",
                        "content": query
                })

        history.append({
                        "role": "assistant",
                        "content": data["Response"]
                })
        save_history(history)
        print(f"AI: {data['Response']}")
        return data['Response']
    except Exception as e:
        print(f"Model failed:", e)
        return "Model Failed."