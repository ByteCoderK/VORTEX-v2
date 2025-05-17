import os
import sys

project_root = os.path.abspath("C:\\Users\\User One\\Desktop\\VORTEX-v2")
sys.path.append(project_root)

# commands
from commands.greet import greet
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
        query, queryList = listen()
        response = route_command(query, queryList)
        
        if response:
            speak(response)
        
        elif any(word in query.lower() for word in ['stop', 'exit', 'quit', 'close', 'deactivate']):
            speak("Goodbye Master.")
            print_colored("\n======================== | DEACTIVATED | ======================", Color.RED)
            sys.exit()
        else:
            print_colored("| VORTEX : PASS-BY", Color.RED)

if __name__ == '__main__':
    logic()
