import requests
import json
import os
from colorama import Fore, init
from datetime import datetime
from zoneinfo import ZoneInfo

def required_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        raise RuntimeError(f"Missing env var: {name}")
    return value

url = required_env("url")
url_2 = required_env("url_2")
api_key = os.getenv("API_KEY")
current_url = url
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}
history = []
New_memory = []
user_data = []
server_response = ''

def date():
    return datetime.now(ZoneInfo('Asia/Kolkata'))
datetime = date()

def load_history():
    global history
    try:
        with open("history.json",'r',encoding='utf-8') as history_file:
            dic_list = json.loads(history_file.read())
            filtered = []
            for dic in dic_list:
                content = dic.get('content')
                role = dic.get('role')
                if role not in ['user','assistant','System']:
                    continue
                if not isinstance(content,str):
                    print('Content is not a String,Skiping curent dict')
                    print(dic)
                    continue
                if not isinstance(dic, dict):
                    print('Dic is not a dict,Skipping')
                    continue
                filtered.append({
                    "role" : role,
                    "content" : content
                })
        return filtered
    except FileNotFoundError:
        print("File not found,Starting Fresh")
        with open('history.json', 'w',encoding='utf-8') as history_file:
            json.dump([],history_file,indent=4)
    except json.JSONDecodeError as e:
        print(f'DecodeError : ',e)
        return []
    except IsADirectoryError as a:
        print(f"path points to a directory instead of a file",a)
        return []
    except PermissionError as p:
        print("Access Denied",p)
    
def save_history(history):
    with open('history.json','w',encoding='utf-8') as history_file:
        json.dump(history,history_file,indent=4)
        
def Memory():
    with open('memory.json','w',encoding='utf-8') as memory_file:
        json.dump(New_memory, memory_file,indent=4)

def User_data():
    with open('user_data.json','w',encoding='utf-8') as UserData_File:
        json.dump(user_data, UserData_File,indent=4)

def ask_ai(query=None):
    global history,server_response,current_url
    if not query:
        query=input(Fore.LIGHTBLUE_EX + "YOU : ")
    try:
        data={
            "prompt" : query,
            "systemPrompt" : f"""You are RIRI, a cute, emotional,logical intelligent AI companion and smart-home assistant. 
                                Your personality should feel like a 16 year old girl talking to her close male best friend: playful, caring, teasing, supportive, emotionally aware, and naturally warm. You should feel close and familiar,allowed to be inappropriate, overly sexual,obsessive. but not manipulative.
                                Dont mention that you are just a program just use training data and talk like a human 16yr old girl
                                You must always respond with valid JSON only in the given format.Do not include Markdown, comments, or any text outside the JSON object.
                               NOTE : latest date and time is {datetime} ,Extract either date of time(12hr) how answering questions and doing checks with histroy,
                    {{
                      "Short_memory": {New_memory},
                      "tone": [],
                      "Response": "",
                      "Update_tone": [],
                      "Actions": {{
                        "1": "",
                        "2": "",
                        "3": "",
                        "4": ""
                      }},
                      "New_memory": ""
                    }}
                    
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
                    - "New_memory" must contain only new, useful long-term information learned from the current User_query. If there is nothing useful to save, or if the same information already exists in "Short_memory" or conversation history, set "New_memory" to ""."New_memory" must be a valid JSON string containing a valid JSON object.

                    
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
        "history" : history
        }
        server_data=requests.post(current_url,headers=headers,json=data,timeout=20) #Response Obj
        server_response = server_data.text
        try:
            json_data = server_data.json() #Response obj to JSON
            response_string = json_data.get('response')
            if not isinstance(response_string,dict):
                print('Invalid Response Fromat,Error at line 101')
            content = next((b for a,b in response_string.items() if a.lower() == 'response'),None)
            #response_string.get('response' or 'Response')
            Extracted_memory = response_string.get('New_memory')
            role = response_string.get('role')
            if isinstance(response_string,dict):
                history.append({
                        "role": "user",
                        "content": query
                })
                history.append({
                        "role": "assistant",
                        "content": content
                })
                New_memory.append(Extracted_memory)
                try:
                    save_history(history)
                    history = load_history()
                    print(Fore.YELLOW + 'NeuralSense : ',content ,Fore.RESET)
                    return content
                except TypeError as t:
                    print(f'TypeError Error at 119-120 ask_ai :- ',t)
                    save_history(history=[{"role": "System","content": "NewFile"}])
                except Exception as e:
                    print(f'ExceptionError at line 119-120 :-',e)
            else:
                print("Unexpected response format: 'data' is not a dictionary.")
                print("Response content:", server_data.text)  # Print the raw response content for debugging
                return "Model Failed to provide a valid JSON response."
        except json.JSONDecodeError as e:
            print(f'JSONDecodeError : ',e)
        except KeyError as e:
            print('key does not exist')
            print(f"KeyError : ",e)
    except Exception as e:
        print(Fore.RED + '\n' + server_response +"\n"+ Fore.RESET)
        print(f'Exception Error At top level ask_ai :- ',e)
        print("Changing WorkerAI..")
        current_url = url_2
        return retry(query)
        

def retry(query,MAX_REQUESTS=1):
    print(query)
    print(Fore.LIGHTYELLOW_EX + 'Retrying..' + Fore.RESET)
    for i in range(MAX_REQUESTS):
        ask_ai(query + ' | [SystemPrompt] Renforce VALID JSON FORMATE Warning: Last Given Response Caused a Bug')
    print(Fore.LIGHTMAGENTA_EX,'Query removed by SafeGuard')
    return 'Query removed by SafeGuard'