import asyncio
import edge_tts
import uuid
import os
from playsound import playsound
from colorama import Fore, Back, Style , init
init()


name = "| VORTEX : "
voice = "en-GB-RyanNeural"
rate = "-6%"
pitch = "-25Hz"
#-------------------------
class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# ------------------------
async def speech_setting(text, voice="en-GB-RyanNeural", rate="-10%", pitch="-2Hz"):
    temp_filename = f"{uuid.uuid4()}.mp3"
    communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate, pitch=pitch)
    await communicate.save(temp_filename)
    playsound(temp_filename)
    os.remove(temp_filename)

# 🛠 Renamed this wrapper to avoid overwriting the async function
def speak(text):
    try:
        print(text)
        asyncio.run(speech_setting(text, voice, rate, pitch))  # uses global vars
    except Exception as e:
        print(f"{name}Error: {e}")

def speakOnly(text):
    asyncio.run(speech_setting(text, voice, rate, pitch))  # also uses global vars
    
def printOnly(text):
    print(f"{name}", text)
