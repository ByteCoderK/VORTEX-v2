import os
import sys
import logging
import random
from concurrent.futures import ThreadPoolExecutor, TimeoutError


standby_word = ["standby","preparing","engaging", "processing", "charging","optimizing", "booting up", "syncing", "initializing", "configuring", "diagnosing","executing", "operating", "synchronizing"]
standby_msg = "Alright Master, " + random.choice(standby_word) + "..."

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('vortex_debug.log'),
        logging.StreamHandler()
    ]
)

project_root = os.path.abspath("C:\\Users\\User One\\Desktop\\VORTEX-v2")
sys.path.append(project_root)
logging.debug(f"Project root set to: {project_root}")

# commands
try:
    from commands.greet import greet
    from commands.date import date
    from commands.time import current_time
    from commands.Weather import live_weather
    from commands.Music import play_music
    from commands.NeuralCore import *
    logging.debug("Command imports successful")
except ImportError as e:
    logging.error(f"Command import failed: {str(e)}")
    raise

# core
try:
    from core.NetworkCheckerProtocol import *
    from core.Voice import *
    from core.Listener import *
    from core.NeuroCache import *
    logging.debug("Core imports successful")
except ImportError as e:
    logging.error(f"Core import failed: {str(e)}")
    raise

def route_command(query: str, queryList: list[str]):
    logging.info(f"Processing query: '{query}' with tokens: {queryList}")
    query = query.lower()

    try:
        if "time" in queryList:
            result = current_time()
            logging.debug(f"Time result: {result}")
            return result, None
            
        elif "date" in queryList:
            result = date()
            logging.debug(f"Date result: {result}")
            return result, None
            
        elif "music" in queryList or "play" in queryList:
            result = play_music()
            logging.debug(f"Music result: {result}")
            return result, None
            
        elif "weather" in queryList:
            city = input("Specify the city: ")
            logging.debug(f"Weather check for city: {city}")
            result = live_weather(city)
            logging.debug(f"Weather result: {result}")
            return result, None

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






        else:
            logging.info("Executing AI and memory protocols")
            
            with ThreadPoolExecutor(max_workers=2) as executor:
                # Log before submission
                logging.debug("Submitting AI task")
                ai_future = executor.submit(ask_ai, query, keys["KEY_1"], True)
                
                logging.debug("Submitting memory task")
                memory_future = executor.submit(rememberMeProtocol, query, keys["KEY_1"])
                
                try:
                    # Get results with timeout
                    ai_result = ai_future.result(timeout=10)
                    logging.debug(f"AI returned: {ai_result}")
                    
                    memory_result = memory_future.result(timeout=10)
                    logging.debug(f"Memory returned: {memory_result}")
                    
                    return ai_result, memory_result
                    
                except TimeoutError:
                    logging.error("Thread execution timed out!")
                    return "AI timeout", "Memory timeout"
                    
                except Exception as e:
                    logging.error(f"Thread execution failed: {str(e)}")
                    return f"AI error: {str(e)}", f"Memory error: {str(e)}"
                    
    except Exception as e:
        logging.critical(f"Unexpected error in route_command: {str(e)}")
        return f"Command error: {str(e)}", None