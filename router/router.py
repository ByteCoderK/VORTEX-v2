import os
import sys
import logging
import random
from concurrent.futures import ThreadPoolExecutor, TimeoutError

standby_word = ["standby", "preparing", "engaging", "processing", "charging",
                "optimizing", "booting up", "syncing", "initializing",
                "configuring", "diagnosing", "executing", "operating",
                "synchronizing"]
standby_msg = "Alright Master, " + random.choice(standby_word) + "..."

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('vortex_debug.log'),
              logging.StreamHandler()]
)

project_root = os.path.abspath("C:\\Users\\User One\\Desktop\\VORTEX-v2")
sys.path.append(project_root)
logging.debug(f"Project root set to: {project_root}")

# routine imports
try:
    from routines.routine_parser import *
    from routines.routine_db import *
    logging.debug("routine import successful")
except ImportError as e:
    logging.error(f"routine import failed: {str(e)}")
    raise


# COMMANDS
try:
    # FIXED: import the CLASS, not the function
    from commands.XAUTOMATION import ESPController

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


# core imports
try:
    from core.Voice import *
    from core.Listener import *
    from core.NeuroCache import *
    logging.debug("Core imports successful")
except ImportError as e:
    logging.error(f"Core import failed: {str(e)}")
    raise


# INIT MQTT CONTROLLER
esp = ESPController(
    broker="c4f73c571367445282f1ae6cd0e5e0ce.s1.eu.hivemq.cloud",
    port=8883,
    username="VORTEX",
    password="ffc-5DF0FSD9AS8-e./';..ls./'lp./';..l-iucfbYwaSDewiaubv-lliot",
    topic_cmd="vortex/relay1",
    topic_feedback="vortex/feedback"
)


def route_command(query: str, queryList: list[str]):
    logging.info(f"Processing query: '{query}' with tokens: {queryList}")
    memory_data = rememberMeProtocol(query)
    query = query.lower()
    routine = parse_routine(query)

    try:

        # ------------------- SIMPLE COMMANDS ----------------------

        if "time" in queryList:
            return current_time(), None

        elif "date" in queryList:
            return date(), None

        elif "music" in queryList or "play" in queryList:
            return play_music(), None

        elif "weather" in queryList:
            city = input("Specify the city: ")
            return live_weather(city), None

        # ------------------- ROOM CONTROLS ----------------------

        # TURN ON
        if "turno" in queryList or "onm" in queryList:

            if "light" in queryList:
                esp.RoomControl(1, "ON")
                return "Light is now on", None

            if "wind" in queryList:
                esp.RoomControl(2, "ON")
                return "Wind is now on", None

            if "ambient" in queryList:
                esp.RoomControl(3, "ON")
                return "Ambient Light is now on", None

            if "socket" in queryList:
                esp.RoomControl(4, "ON")
                return "Socket is now on", None

            if "all" in queryList:
                for i in range(1, 5):
                    esp.RoomControl(i, "ON")
                return "All Devices are now on", None

        # TURN OFF
        if "turno" in queryList or "offm" in queryList:

            if "light" in queryList:
                esp.RoomControl(1, "OFF")
                return "Light is now off", None

            if "wind" in queryList:
                esp.RoomControl(2, "OFF")
                return "Wind is now off", None

            if "ambient" in queryList:
                esp.RoomControl(3, "OFF")
                return "Ambient Light is now off", None

            if "socket" in queryList:
                esp.RoomControl(4, "OFF")
                return "Socket is now off", None

            if "all" in queryList:
                for i in range(1, 5):
                    esp.RoomControl(i, "OFF")
                return "All Devices are now off", None

        # ------------------- AI + MEMORY ----------------------

        with ThreadPoolExecutor(max_workers=3) as executor:

            ai_future = executor.submit(ask_ai, query, keys["KEY_1"], True)
            routine_future = executor.submit(parse_routine, query)
            memory_future = executor.submit(write_memory, memory_data)

            try:
                return (
                    ai_future.result(timeout=10),
                    memory_future.result(timeout=10),
                    routine_future.result(timeout=10)
                )

            except TimeoutError:
                return "AI timeout", "Memory timeout", "Routine timeout"

            except Exception as e:
                return f"AI error: {e}", f"Memory error: {e}", f"Routine error: {e}"

    except Exception as e:
        logging.critical(f"Unexpected error in route_command: {str(e)}")
        return f"Command error: {str(e)}", None
