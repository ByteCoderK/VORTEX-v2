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

ConnectionProtocol()

def logic():
    speak(greet())

    while True:
        listen()
        query, queryList = listen()
        if not query:  
            continue

        query = query.lower()

        if "time" in queryList:
            speak(current_time())

        elif "date" in queryList:
            speak(date())

        elif any(word in query.lower() for word in ['stop', 'exit', 'quit', 'close', 'deactivate']):
            speak("Goodbye Master.")
            print_colored("\n======================== | DEACTIVATED | ======================", Color.RED)
            sys.exit()

        elif query.strip() == "":
            print_colored("| VORTEX : I'm sorry, Master. I didn't understand that. Could you please repeat?", Color.YELLOW)
        else:
            print_colored("| VORTEX : PASS-BY", Color.RED)

if __name__ == '__main__':
    logic()
