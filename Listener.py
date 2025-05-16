import sys
import os
import speech_recognition as sr
sys.path.append(os.path.abspath("C:\\Users\\User One\\Desktop\\VORTEX-v2\\core\\Voice.py"))
from Voice import *

r = sr.Recognizer()
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