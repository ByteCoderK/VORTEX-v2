import os
import sys
import logging
from concurrent.futures import ThreadPoolExecutor, TimeoutError

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