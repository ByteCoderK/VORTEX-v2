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
        logger.debug("Deleting *all* jobs")
        schedule.clear()
        routines = load_routines()
        logger.info("Reloading routines: %d routines found", len(routines))
        for r in routines:
            register_routine(r)
        logger.info("[ROUTINE] Reload complete.")

def register_routine(routine):
    t = routine.get("trigger", {})
    action = routine.get("action", {})
    value = t.get("value")

    # guard invalid times
    if not value:
        logger.warning("Skipping routine with no time value: %s", routine)
        return

    freq = t.get("frequency", "once")
    logger.info("Registering routine: freq=%s time=%s action=%s", freq, value, action)

    # Wrap schedule.at calls with try/except to prevent crash on bad formats
    try:
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
            # 'once' or unknown: schedule for the time today (schedule library doesn't support one-off directly)
            schedule.every().day.at(value).do(wrap_execute_once, action, routine)
    except schedule.ScheduleValueError as sve:
        logger.warning("Invalid time format for routine %s: %s. Skipping.", routine, sve)
    except Exception as e:
        logger.exception("Failed to schedule routine %s: %s", routine, e)

def wrap_execute(action):
    logger.info("Executing routine action now: %s", action)
    try:
        execute_action(action)
    except Exception as e:
        logger.exception("Error executing action: %s", e)

def wrap_execute_once(action, routine):
    """
    Execute the action and then remove the routine from persistent storage so it's truly one-time.
    """
    logger.info("Executing one-time routine action now: %s", action)
    try:
        execute_action(action)
    except Exception as e:
        logger.exception("Error executing one-time action: %s", e)
    # after executing, delete the routine from DB
    try:
        from routines.routine_db import load_routines, save_routines
        routines = load_routines()
        # find and remove matching routine (simple equality)
        try:
            routines.remove(routine)
            save_routines(routines)
            logger.info("One-time routine removed from DB after execution.")
            # reload schedule to remove any duplicate jobs
            reload_routines()
        except ValueError:
            logger.warning("One-time routine not found in DB; couldn't remove.")
    except Exception:
        logger.exception("Failed to remove one-time routine after execution.")

def start_engine():
    routines = load_routines()
    logger.info("Routine engine loading %d routines", len(routines))
    for r in routines:
        register_routine(r)
    logger.info("[ROUTINE] Engine started. Waiting for schedule...")
    while True:
        schedule.run_pending()
        time.sleep(1)