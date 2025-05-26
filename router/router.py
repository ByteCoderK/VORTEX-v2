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

    # Date query
    elif "date" in queryList:
        return date()

    # Music playback
    elif "music" in queryList or "play" in queryList:
        return play_music()

    # Weather info
    elif "weather" in queryList:
        speak("Please specify the city for which you want the weather information.")
        city = input("Enter city name: ")  # TODO: replace with dynamic input
        return live_weather(city)  # TODO: replace with dynamic city input

    # Unknown / fallback
    else:
        t1.start()
        t2.start()
        
        t1.join()
        t2.join()