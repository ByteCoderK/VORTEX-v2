import os
import sys

project_root = os.path.abspath("C:\\Users\\User One\\Desktop\\VORTEX-v2")
sys.path.append(project_root)

# commands
from commands.greet import greet
from commands.NeuralCore import *
# core
from core.NetworkCheckerProtocol import *
from core.Voice import *
from core.Listener import *

#router
from router.router import route_command


ConnectionProtocol()

def logic():
    speak(greet())

    while True:
        try:
            query, queryList = listener()
            response = route_command(query, queryList)
        except Exception as UnboundLocalError:
            print("Audio not clear enough/Capture error")
        

        if response:
            speak(response)
        
        elif any(word in query.lower() for word in ['stop', 'exit', 'quit', 'close', 'deactivate']):
            speak("Goodbye Master.")
            print_colored("\n======================== | DEACTIVATED | ======================", Color.RED)
            sys.exit()
        else:
            print_colored("| VORTEX :  " + ask_ai(query), Color.CYAN)

if __name__ == '__main__':
    logic()
