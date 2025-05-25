import os
import sys

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
        return ask_ai(query)