# routines/routine_engine.py
import os
import sys
import threading
import time
import logging
from datetime import datetime, timedelta, timezone
import sqlite3
import schedule

MODULE_DIR = os.path.dirname(__file__)
sys.path.append(MODULE_DIR)

from routines.routine_db import load_routines
from routines.routine_executor import execute_action

logger = logging.getLogger("routine_engine")
logging.basicConfig(level=logging.INFO)

schedule_lock = threading.Lock()

# IST timezone
IST = timezone(timedelta(hours=5, minutes=30))

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
    freq = t.get("frequency", "once")

    if not value:
        logger.warning("Skipping routine with no time value: %s", routine)
        return

    logger.info("Registering routine: freq=%s time=%s action=%s", freq, value, action)

    # Convert HH:MM string to IST datetime
    hour, minute = map(int, value.split(":"))
    now_ist = datetime.now(IST)
    run_time = now_ist.replace(hour=hour, minute=minute, second=0, microsecond=0)

    if freq == "once":
        if run_time < now_ist:
            run_time += timedelta(days=1)  # schedule for tomorrow if time passed
        delay = (run_time - now_ist).total_seconds()
        threading.Timer(delay, wrap_execute, args=(action,)).start()
    else:
        # daily or day-specific routines
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
            logger.warning("Unknown frequency '%s', scheduling daily by default", freq)
            schedule.every().day.at(value).do(wrap_execute, action)


def wrap_execute(action):
    logger.info("[ROUTINE] Executing action: %s", action)
    try:
        execute_action(action)
        logger.info("[ROUTINE] Action executed successfully")
    except Exception as e:
        logger.exception("[ROUTINE] Failed to execute action: %s", e)


def start_engine():
    logger.info("[ROUTINE] Starting engine...")
    reload_routines()
    while True:
        with schedule_lock:
            schedule.run_pending()
        time.sleep(1)