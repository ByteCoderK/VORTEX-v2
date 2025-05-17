import sys
import os
import speech_recognition as sr
from colorama import Fore, Back, Style , init
init()

class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


def print_colored(text, color):
    print(color + text + Color.RESET)

r = sr.Recognizer()
queryList = []
searchKey = ""
query = ''
bluetooth_headset_index = 1  # Adjust this index according to your Bluetooth headset

def listener():
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
