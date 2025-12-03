# routines/routine_engine.py
import os
import sys
import schedule
import time
import logging
import threading
from datetime import datetime
MODULE_DIR = os.path.dirname(__file__)
sys.path.append(MODULE_DIR)

from routines.routine_db import load_routines
from routines.routine_executor import execute_action

logger = logging.getLogger("routine_engine")
schedule_lock = threading.Lock()

def reload_routines():
    """Clear existing jobs and load fresh routines from JSON."""
    with schedule_lock:
        schedule.clear()
        routines = load_routines()
        logger.info("Reloading routines: %d routines found", len(routines))
        for r in routines:
            register_routine(r)
        logger.info("[ROUTINE] Reload complete.")

def register_routine(routine):
    t = routine["trigger"]
    action = routine["action"]
    value = t.get("value")

    # guard invalid times
    if not value:
        logger.warning("Skipping routine with no time value: %s", routine)
        return

    freq = t.get("frequency", "once")
    logger.info("Registering routine: freq=%s time=%s action=%s", freq, value, action)

    if freq == "daily":
        schedule.every().day.at(value).do(wrap_execute, action)
    elif freq == "monday":
        schedule.every().monday.at(value).do(wrap_execute, action)
    elif freq == "tuesday":
        schedule.every().tuesday.at(value).do(wrap_execute, action)
    elif freq == "wednesday":
        schedule.every().wednesday.at(value).do(wrap_execute, action)
    elif freq == "thursday":
        schedule.every().thursday.at(value).do(wrap_execute, action)
    elif freq == "friday":
        schedule.every().friday.at(value).do(wrap_execute, action)
    elif freq == "saturday":
        schedule.every().saturday.at(value).do(wrap_execute, action)
    elif freq == "sunday":
        schedule.every().sunday.at(value).do(wrap_execute, action)
    else:
        schedule.every().day.at(value).do(wrap_execute, action)

def wrap_execute(action):
    logger.info("Executing routine action now: %s", action)
    try:
        execute_action(action)
    except Exception as e:
        logger.exception("Error executing action: %s", e)

def start_engine():
    routines = load_routines()
    logger.info("Routine engine loading %d routines", len(routines))
    for r in routines:
        register_routine(r)
    logger.info("[ROUTINE] Engine started. Waiting for schedule...")
    while True:
        schedule.run_pending()
        time.sleep(1)