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
            #reads the content of history.json and parses it as JSON, storing it in the variable history as python list of dictionaries
            history = json.load(history_file)
    except FileNotFoundError:
        print("history.json not found. Starting with an empty history.")
        return []
    except json.JSONDecodeError:
        print("history.json is not valid JSON.")
        return []

    if not isinstance(history, list):
        return []
    
    filtered_history = []
    for message in history:
        if not isinstance(message, dict):
            continue    
        role = message.get("role")
        content = message.get("content")

        if role not in ["user", "assistant"]:
            continue

        if not isinstance(content, str):
            continue

        filtered_history.append({
            "role": role,
            "content": content
        })
    return filtered_history
history = load_history()

def save_history(history):
    with open('history.json','w',encoding='utf-8') as history_file:
        #converts the history list to a JSON object and writes it to the file with indentation for readability
        json.dump(history, history_file,indent=4)
        

def ask_ai(query=None):
    global history
    if not query:
        query = input("You: ")
    try:
        data = {
                "prompt": query,
                "systemPrompt": """You are Atas.You must always respond with valid JSON only in the given format.Do not include Markdown, explanations, comments, or any text outside the JSON object.
                    {
                      "Short_memory": "example.json",
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
        server_output = requests.post(url, headers=headers, json=data, timeout=20)
        try:
            output_json = server_output.json()
            print("Raw response from server:", output_json)  # Debugging line to see the raw response
        except json.JSONDecodeError as error:
            print("Failed to decode JSON response:", error)
            print("Response content:", server_output.text)  # Print the raw response content for debugging
            return "Model Failed."
        except Exception as e:
            print("An error occurred while processing the response:", e)
            return "Model Failed."
        data = output_json.get('response')
        if not isinstance(data, dict):
            print("Unexpected response format: 'data' is not a dictionary.")
            print("Response content:", output_json)  # Print the raw response content for debugging
            return "Model Failed to provide a valid JSON response."
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
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return "Model Failed."
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON response: {e}")
        return "Model Failed."
    except Exception as e:
        print(f"Model failed:", e)
        return "Model Failed."
