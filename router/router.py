import os
import sys
import logging
import random
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import threading 

logger = logging.getLogger("vortex.router")

standby_word = ["standby", "preparing", "engaging", "processing", "charging",
                "optimizing", "booting up", "syncing", "initializing",
                "configuring", "diagnosing", "executing", "operating",
                "synchronizing"]
standby_msg = "Alright Master, " + random.choice(standby_word) + "..."

if not logger.handlers:
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.FileHandler('vortex_debug.log'),
                  logging.StreamHandler()]
    )
# routine imports
try:
    from routines.routine_engine import start_engine, reload_routines
    from routines.routine_parser import parse_routine
    from routines.routine_db import *
    logger.debug("routine import successful")
except ImportError as e:
    logger.error("routine import failed: %s", str(e))
    raise

# COMMANDS
try:
    from commands.XAUTOMATION import ESPController
    from commands.Weather import live_weather
    from core.NeuralCore import *
    logger.debug("Command imports successful")
except ImportError as e:
    logger.error("Command import failed: %s", str(e))
    raise
threading.Thread(target=start_engine, daemon=True).start()

def required_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        raise RuntimeError(f"Missing env var: {name}")
    return value

broker = required_env('broker')
username = required_env('username')
password = required_env('password')
topic_cmd = required_env('topic_cmd')
topic_feedback = required_env('topic_feedback')

# INIT MQTT CONTROLLER
esp = ESPController(
    broker=broker,
    port=8883,
    username=username,
    password=password,
    topic_cmd=topic_cmd,
    topic_feedback=topic_feedback
)

def route_command(query: str, queryList: list[str]):
    logger.info("Processing query: '%s' with tokens: %s", query, queryList)
    #memory_data = rememberMeProtocol(query)
    query = query.lower()
    

    try:
        # ------------------- SIMPLE COMMANDS ----------------------

        if "weather" in queryList:
            logger.info("Weather branch selected")
            city = input("Specify the city: ")
            return live_weather(city), None
        #-----------------------------------------------------------
        with ThreadPoolExecutor(max_workers=3) as executor:
            logger.debug("Submitting AI and routine parsing tasks")
            ai_future = executor.submit(ask_ai, query)
            routine_future = executor.submit(parse_routine, query)
            # memory_future = executor.submit(write_memory, memory_data)
            try:
                ai_response = ai_future.result(timeout=10)
                # memory_future.result(timeout=10)
                routine_result = routine_future.result(timeout=10)
                logger.debug("AI and routine parsing completed")
                # Only add routine if parse_routine returned a valid routine
                if routine_result and routine_result.get("trigger", {}).get("value"):
                    try:
                        rid = add_routine(
                            routine_result["trigger"]["value"],
                            routine_result["trigger"]["frequency"],
                            routine_result["action"]["device"],
                            routine_result["action"]["relay"],
                            routine_result["action"]["state"]
                        )
                        logger.info("Routine added successfully, rid=%s", rid)
                        reload_routines()
                    except Exception as e:
                        logger.exception("Routine add error: %s", e)
                else:
                    logger.debug("No routine detected in query.")
                logger.info("route_command completed successfully")
                return ai_response
            except TimeoutError:
                logger.error("AI or memory operation timed out")
                return "Processing timed out", None
    except Exception as e:
        logger.exception("route_command fatal error: %s", e)
        return "Critical error during command routing", None
