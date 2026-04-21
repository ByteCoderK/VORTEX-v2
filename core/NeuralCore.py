import os 
import requests
import json 
url = "https://ai.asherapream5.workers.dev/"
headers = {
        "Authorization": "Bearer :-@ZAs|T*L!<QQ.W7(xvj#A",
        "Content-Type": "application/json",
    }
history = []

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

def ask_ai(query=None):
    global history
    if not query:
        query=input("YOU : ")
    try:
        data={
            "prompt" : query,
            "systemPrompt" : """You are Atas.You must always respond with valid JSON only in the given format.Do not include Markdown, comments, or any text outside the JSON object.
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
        "history" : history
        }
        server_data=requests.post(url,headers=headers,json=data,timeout=20) #Response Obj
        try:
            json_data = server_data.json() #Response obj to JSON
            response_string = json_data.get('response')
            if not isinstance(response_string,dict):
                print('Invalid Response Fromat,Error at line 101')
                return 
            content = response_string.get('Response')
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
                try:
                    save_history(history)
                    history = load_history()
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
        print(f'Exception Error At top level ask_ai :- ',e)    