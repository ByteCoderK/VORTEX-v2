import os
import sys

project_root = os.path.abspath("C:\\Users\\User One\\Desktop\\VORTEX-v2")
sys.path.append(project_root)

#commands imports
from commands.greet import *
from commands.date import *
from commands.time import *
from commands.Weather import *
from commands.Music import *

#core imports
from core.NetworkCheckerProtocol import *
from core.Voice import *

ConnectionProtocol()

# print_colored("| VORTEX : Error Device Offline.",Color.RED) FOR ERROR MESSAGE




def logic():
    speak(greet())
    global NAME_EXTRACTION_1, RECEIVER_NAME, RECEIVER_NAME_protocol2,reminderTime,searchKey
    global reminderMessage,reminderTime,reminderTimeAsk
    global query,queryList
    while True:
        #listen()
        query = query.lower()
        
        if "time" in queryList:
            speak(current_time())
        elif "date" in queryList:
            speak(date())

        #elif any(sentance in query for sentance in ['what is the weather',"what's the weather"]):
         #   try:
          #      speak("Please specify the city: ")
           #     city = input('| USER  :  ')
            #    live_weather(city)
            #except Exception as e:
             #   speakOnly("Error Device Offline.")
              #  print_colored("| VORTEX : Error Device Offline.",Color.RED)

        #elif "reminder" in queryList:
         #   speak("Sure, what's the reminder?")
          #  reminderTimeAsk = input("USER  : ")
           # if "everyday" in reminderMessage:
            #    pass
            #else:
             #   numExtraction = reminderTimeAsk.split()
              #  for x in numExtraction:
               #     if x.isdigit():  # Check if x is a digit
                #        reminderTime.append(int(x))
                #for y in numExtraction:
                 #   if "am" in y.lower() or "pm" in y.lower():
                  #      reminderTime.append(y)
                #print(reminderTime)

        elif any(word in query.lower() for word in ['stop', 'exit', 'quit', 'close', 'deactivate']):
            speak("GoodBye Master..")
            print_colored("\r======================== |      DEACTIVATED     | ======================\n",Color.RED)
            sys.exit()

        elif query.strip() == "":
            print_colored("| VORTEX : I'm sorry, Master. I didn't understand that. Could you please repeat or try a different command?", Color.YELLOW)
            print(query)
        else:
            print_colored("| VORTEX :  PASS-BY ", Color.RED)
            pass
if __name__ == '__main__':
    logic()
else: 
    print("WARNING : Running as imported Module")
    logic()