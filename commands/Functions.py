import serial
import datetime
import os
import sys
import random
import time
import requests
import webbrowser
from requests import get
sys.path.append(os.path.abspath("A:\\VORTEX\\Brain\\Voice.py"))
sys.path.append(os.path.abspath("A:\\VORTEX\\Brain\\NetworkCheckerProtocol.py"))
from colorama import Fore, Back, Style , init
init()
import asyncio
import edge_tts
import uuid
import os
from playsound import playsound

try:
    ser = serial.Serial('COM3', 9600, timeout=1)
except Exception as e:
    pass
#====================================================================================

# Initialize Liberies
#text to speech
name = "| VORTEX : "
voice = "en-GB-RyanNeural"
rate = "-6%"
pitch = "-25Hz"
#------------------------
async def speech_setting(text, voice="en-GB-RyanNeural", rate="-10%", pitch="-2Hz"):
    temp_filename = f"{uuid.uuid4()}.mp3"
    communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate, pitch=pitch)
    await communicate.save(temp_filename)
    playsound(temp_filename)
    os.remove(temp_filename)

# 🛠 Renamed this wrapper to avoid overwriting the async function
def speak(text):
    try:
        asyncio.run(speech_setting(text, voice, rate, pitch))  # uses global vars
    except Exception as e:
        print(f"{name}Error: {e}")

#====================================================================================
# Variable
MESSAGE = ""
reminderMessage = ""
reminderTime = []
reminderTimeAsk = ""
numExtraction = ""
number = [0,1,2,3,4,5,6,7,8,9]
greetings = ['hello','hey','hi','hai']


    
#====================================================================================
class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def ArdinoTest():
    try:
        control_relay(1, '2')
        print(Fore.GREEN + "\r======================== | SmartHomeConnected | ======================" + Fore.RESET)
    except Exception as e:
        print(Fore.RED + "\r======================== |   SmartHomeError   | ======================" + Fore.RESET)
        

def speak(text):
    try:
        asyncio.run(speech_setting(text, voice, rate, pitch))  # uses global vars
    except Exception as e:
        print(f"{name}Error: {e}")

    
def printOnly(text):
    print(f"{name}", text)

def speakOnly(text):
    asyncio.run(speech_setting(text, voice, rate, pitch))  # also uses global vars


def date():
    date = datetime.datetime.now()
    speak(date)

def current_time():
    current_time = datetime.datetime.now()
    current_time_str = current_time.strftime("%I:%M %p")
    speak("Current time is: " + current_time_str)
    print(current_time_str)

def live_weather(city):
    api_key = "25bd76ae6cf5eb2e0e71604ff5eb2bcd"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    # Check the response code
    if response.status_code == 200:
        # Fetch weather description, temperature, humidity, and wind speed
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        # Speak the weather information
        speak(f"The current weather in {city} is {weather_description},\n\t   The temperature is {temperature} degrees Celsius,\n\t   The humidity is {humidity} percent,\n\t   The wind speed is {wind_speed} meters per second.")
    else:
        # Speak an error message if the response code is not 200 (e.g., city not found)
        speak("Sorry, I couldn't fetch the weather information for the specified city.")
