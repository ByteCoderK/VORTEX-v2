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

# core
from core.NetworkCheckerProtocol import *
from core.Voice import *
from core.Listener import *

def route_command(query: str, queryList: list[str]) -> str:
    query = query.lower()

    # Greetings
    if any(word in queryList for word in ["hi", "hello", "hey"]):
        return greet()

    # Time query
    elif "time" in queryList:
        return current_time()

    # Date query
    elif "date" in queryList:
        return date()

    # Music playback
    elif "music" in queryList or "play" in queryList:
        return play_music()

    # Weather info
    elif "weather" in queryList:
        return live_weather("delhi")  # TODO: replace with dynamic city input

    # Exit command
    elif any(word in query for word in ["exit", "stop", "quit", "close", "deactivate"]):
        return "exit"

    # Unknown / fallback
    else:
        return None