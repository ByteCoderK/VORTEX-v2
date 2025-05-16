import sys
import time
import os
import serial
import requests
from colorama import Fore, Back, Style , init
init()
sys.path.append(os.path.abspath("C:\\User\\User One\\Desktop\\VORTEX-v2\\core\\Voice.py"))
from Voice import *
loading = True
loadTime = 0
try:
    ser = serial.Serial('COM3', 9600, timeout=1)
except Exception as E:
    pass

# ----------------------------------------------------------------------------------------------------------------------------------------------
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
# ----------------------------------------------------------------------------------------------------------------------------------------------
def ArdinoTest():
    try:
        CR(1, '2')
        print_colored("\r======================== | SmartHomeConnected | ======================",Color.GREEN)
    except Exception as e:
        print_colored("\r======================== |   SmartHomeError   | ======================",Color.YELLOW)

def CR(relay_number, state):
    command = str(relay_number) + state
    ser.write(command.encode())


def control_relay(relay_number, state):
    try:
        command = str(relay_number) + state
        ser.write(command.encode())
    except Exception as E:
        speakOnly("Apologies, Master. It seems I'm unable to control that hardware at the moment.Would you like me to try something else?")
        print_colored("| VORTEX :  Error: Unable to establish connection with the designated hardware. Please ensure that the device is properly configured and accessible.\n \t   Alternatively, there may be a technical issue preventing communication.",Color.RED)

def print_loading():
    global loading,loadTime
    loading_sprites = ['|', '/', '-', '\\']
    loading_speed = 0.09  # Time in seconds between each sprite update
    laod()
    while loading == True:  # Loop to repeat the animation 10 times
        for sprite in loading_sprites:
            loadTime += 1
            sys.stdout.write(f'\r======================== |      Loading {sprite}     | ======================')
            sys.stdout.flush()  # Flush the output to display immediately
            time.sleep(loading_speed)  # Wait for the specified loading speed
    sys.stdout.write(Fore.GREEN + '\r======================== |      ACTIVATED     | ======================\n' + Fore.RESET)
    try:
        ser = serial.Serial('COM3', 9600, timeout=1)
        print(Fore.GREEN + "\r======================== | SmartHomeConnected | ======================")
    except Exception as ArdinoNegitive:
        ArdinoTest()
    print_colored("\t\t      [VORTEX : Powered by GenoVance]", Color.CYAN)

def laod():
    global loading
    loading = True
    time.sleep(5)
    loading = False

def ConnectionProtocol():
    try:
        print_loading()
        requests.get("https://www.google.com", timeout=3)
        print(Fore.GREEN + '========================| Network: Connected |========================\n' + Fore.RESET)
    except Exception as notConnected:
        print_loading()
        print(Fore.RED + '======================== | Network: Disconnected |======================\n' + Fore.RESET)