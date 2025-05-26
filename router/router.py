import os
import sys
import threading

project_root = os.path.abspath("C:\\Users\\User One\\Desktop\\VORTEX-v2")
sys.path.append(project_root)

# commands
from commands.greet import greet
from commands.date import date
from commands.time import current_time
from commands.Weather import live_weather
from commands.Music import play_music
from commands.NeuralCore import *

# core
from core.NetworkCheckerProtocol import *
from core.Voice import *
from core.Listener import *
from core.NeuroCache import *

first_call = True
t1= threading.Thread(target=ask_ai, args=(query,CURRENT_key,first_call))
t2 = threading.Thread(target=rememberMeProtocol, args=(query,CURRENT_key)) 

def route_command(query: str, queryList: list[str]) -> str:
    query = query.lower()

    if "time" in queryList:
        return current_time()
    elif "date" in queryList:
        return date()
    elif "music" in queryList or "play" in queryList:
        return play_music()
    elif "weather" in queryList:
        speak("Please specify the city for weather info.")
        city = input("Enter city name: ")  # Use your voice input instead of hardcoded input
        return live_weather(city)
    else:
        # Create NEW threads each time (critical fix)
        ai_thread = threading.Thread(target=ask_ai, args=(query, CURRENT_key, True))
        memory_thread = threading.Thread(target=rememberMeProtocol, args=(query, CURRENT_key))
        
        ai_thread.start()
        memory_thread.start()
        
        ai_thread.join()
        memory_thread.join()