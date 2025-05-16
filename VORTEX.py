import speech_recognition as sr
import os
import sys

project_root = os.path.abspath("C:\\Users\\User One\\Desktop\\VORTEX-v2")
sys.path.append(project_root)


from commands.greet import *
from commands.Functions import *
from core.NetworkCheckerProtocol import *
from core.Voice import *

#------------------------
r = sr.Recognizer()
#------------------------
#ConnectionProtocol()

# print_colored("| VORTEX : Error Device Offline.",Color.RED) FOR ERROR MESSAGE
queryList = []
searchKey = ""
query = ''
bluetooth_headset_index = 1  # Adjust this index according to your Bluetooth headset

def listen():
    global query,queryList
    # Capture audio input from the specified Bluetooth headset
    try:
        with sr.Microphone(device_index=bluetooth_headset_index) as source:
                print("Listening..")
                audio = r.listen(source)
                recognizing = True
    except Exception as e:
        print("Error: ", e)
        print_colored("| VORTEX :  Error: Unable to establish connection with the designated hardware. Please ensure that the device is properly configured and accessible.\n \t   Alternatively, there may be a technical issue preventing communication.",Color.RED)
        return
    # Recognize speech using Google Web Speech API
    while recognizing == True:
        try:
            print("Recognizing...")
            Vinput = r.recognize_google(audio)
            query = Vinput
            queryList = query.split()
            print("| USER  :  " + query)
            recognizing = False
            return query,queryList
        except sr.UnknownValueError:
            print("Apologies, the audio wasn't clear enough.")
        break

def logic():
    greetings == greet()
    speak(greetings)
    #DailyReminderLoader()
    global NAME_EXTRACTION_1, RECEIVER_NAME, RECEIVER_NAME_protocol2,reminderTime,searchKey
    global reminderMessage,reminderTime,reminderTimeAsk
    global query,queryList
    while True:
        listen()
        query = query.lower()
        
        if "time" in queryList:
            current_time()
        elif "date" in queryList:
            date()

        #elif any(sentance in query for sentance in ['what is the weather',"what's the weather"]):
         #   try:
          #      speak("Please specify the city: ")
           #     city = input('| USER  :  ')
            #    live_weather(city)
            #except Exception as e:
             #   speakOnly("Error Device Offline.")
              #  print_colored("| VORTEX : Error Device Offline.",Color.RED)

        elif "play music" == query or "play songs" == query or "play a song" == query:
            play_music()

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
    pass
    #:Logic()
else: 
    
    print("WARNING : Running as imported Module")
    #logic()
listen()