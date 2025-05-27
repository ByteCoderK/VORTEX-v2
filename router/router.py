import os
import sys
from concurrent.futures import ThreadPoolExecutor

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


def route_command(query: str, queryList: list[str]) -> str:
    query = query.lower()

    if "time" in queryList:
        return current_time()
    elif "date" in queryList:
        return date()
    elif "music" in queryList or "play" in queryList:
        return play_music()
    elif "weather" in queryList:
        city = input("specify the city:  ")  # Changed from input() to use voice input
        return live_weather(city)
    else:
            # Using ThreadPoolExecutor for proper return value handling
        with ThreadPoolExecutor(max_workers=1) as executor:
                # Submit the AI tas
            ai_future = executor.submit(ask_ai, query, keys["KEY_1"], True)
            # If you need memory processing too:
            #memory_future = executor.submit(rememberMeProtocol, query, CURRENT_key)            
            # Get the AI result
            ai_result = ai_future.result()
            # If using memory:
            #memory_result = memory_future.result()            
            return ai_result