import sys
import os
import random

sys.path.append(os.path.abspath("A:\\VORTEX\\Brain\\VORTEX.py"))
from Brain.VORTEX import queryList,control_relay,speak 

standby_word = ["standby","preparing","engaging", "processing", "charging","optimizing", "booting up", "syncing", "initializing", "configuring", "diagnosing","executing", "operating", "synchronizing"]
standby_msg = "Alright Master, " + random.choice(standby_word) + "..."
def ArdinoControl():
    if queryList[0] == "turn" and queryList[1] == "on":
        if 'light' in queryList:
            speak(standby_msg)
            control_relay(1, '1')  # RELAY 1 ON 
        elif 'fan' in queryList:
            speak(standby_msg)
            control_relay(2, '3')  # RELAY 3 ON
        elif 'tv' in queryList:
            speak(standby_msg)
            control_relay(2, '5')  # RELAY 5 ON
        elif 'monitor' in queryList:
            speak(standby_msg)
            control_relay(2, '7')  # RELAY 7 ON
        elif 'all' in queryList:
            speak(standby_msg)
            control_relay(1, '1'),control_relay(2, '3'),control_relay(2, '5'),control_relay(2, '7')
    # Check if the first word is "off" or "turn off"
    elif queryList[0] == "off" or (queryList[0] == "turn" and queryList[1] == "off"):
        if 'light' in queryList:
            speak("Deactivating device,Please Wait...")
            control_relay(1, '2')  # RELAY 2 OFF
        elif 'fan' in queryList:
            speak("Deactivating device,Standby...")
            control_relay(2, '4')  # RELAY 4 OFF
        elif 'tv' in queryList:
            speak("Deactivating device,Dengaging...")
            control_relay(2, '6')  # RELAY 6 OFF
        elif 'monitor' in queryList:
            speak("Deactivating device,Preparing...")
            control_relay(2, '8')  # RELAY 8 OFF
        elif 'all' in queryList:
            speak("Deactivating all devices, Please wait...")
            control_relay(1, '2'),control_relay(2, '4'),control_relay(2, '6'),control_relay(2, '8')