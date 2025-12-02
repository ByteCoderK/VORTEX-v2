import os
import sys
import logging
import random
from routine_parser import parse_routine
from routine_db import add_routine
from concurrent.futures import ThreadPoolExecutor, TimeoutError
#

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
    from commands.XAUTOMATION import *
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
    from core.Voice import *
    from core.Listener import *
    from core.NeuroCache import *
    logging.debug("Core imports successful")
except ImportError as e:
    logging.error(f"Core import failed: {str(e)}")
    raise

memory_data = rememberMeProtocol(query)


def route_command(query: str, queryList: list[str]):
    logging.info(f"Processing query: '{query}' with tokens: {queryList}")
    query = query.lower()
    routine = parse_routine(query)

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
        
        elif "turn" and "on" in queryList:
            if 'light' in queryList:
                RoomControl(1, 'ON')  # RELAY 1 ON 
                
                return "Light is now on", None 
            elif 'wind' in queryList:
                RoomControl(2, 'ON')  # RELAY 3 ON
                return "Wind is now on", None
            elif 'ambient' in queryList:
                RoomControl(3, 'ON')  # RELAY 5 ON
                return "Ambient Light is now on", None
            elif 'socket' in queryList:
                RoomControl(4, 'ON')  # RELAY 7 ON
                return "Socket is now on", None
            elif 'all' in queryList:
                RoomControl(1, 'ON'),RoomControl(2, 'ON'),RoomControl(3, 'ON'),RoomControl(4, 'ON')
                return "All Devices is now on", None
    # Check if the first word is "off" or "turn off"
        elif "turn" and "off" in queryList:
            if 'light' in queryList:
                RoomControl(1, 'OFF')  # RELAY 1 ON 
                return "Light is now off", None 
            elif 'wind' in queryList:
                RoomControl(2, 'OFF')  # RELAY 3 ON
                return "Wind is now off", None
            elif 'ambient' in queryList:
                RoomControl(3, 'OFF')  # RELAY 5 ON
                return "Ambient Light is now off", None
            elif 'socket' in queryList:
                RoomControl(4, 'OFF')  # RELAY 7 ON
                return "Socket is now off", None
            elif 'all' in queryList:
                RoomControl(1, 'OFF'),RoomControl(2, 'OFF'),RoomControl(3, 'OFF'),RoomControl(4, 'OFF')
                return "All Devices is now off", None

        else:
            logging.info("Executing AI and memory protocols")
            
            with ThreadPoolExecutor(max_workers=3) as executor:
                # Log before submission
                logging.debug("Submitting AI task")
                ai_future = executor.submit(ask_ai, query, keys["KEY_1"], True)
                
                logging.debug("Submitting memory task")
                
                routine_identifier = executor.submit(add_routine,routine)
                
                logging.debug("Submitting query for routine extraction.....")
               
                memory_future = executor.submit(write_memory,memory_data)
                
                try:
                    # Get results with timeout
                    ai_result = ai_future.result(timeout=10)
                    logging.debug(f"AI returned: {ai_result}")
                    
                    routine_result = routine_identifier.result(timeout=10)
                    logging.debug(f"routine_result returned: {routine_result}")
                    
                    
                    memory_result = memory_future.result(timeout=10)
                    logging.debug(f"Memory returned: {memory_result}")
                    
                    return ai_result, memory_result,routine_result
                    
                    
                except TimeoutError:
                    logging.error("Thread execution timed out!")
                    return "AI timeout", "Memory timeout","routine_result timeout"
                    
                    
                except Exception as e:
                    logging.error(f"Thread execution failed: {str(e)}")
                    return f"AI error: {str(e)}", f"Memory error: {str(e)}",f"routine_result: {str(e)}"
                    
    except Exception as e:
        logging.critical(f"Unexpected error in route_command: {str(e)}")
        return f"Command error: {str(e)}", None
    
