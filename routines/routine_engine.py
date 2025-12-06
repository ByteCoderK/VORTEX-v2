# routines/routine_engine.py
import os
import sys
import schedule
import time
import logging
import threading
from datetime import datetime, time as dt_time
from zoneinfo import ZoneInfo

MODULE_DIR = os.path.dirname(__file__)
sys.path.append(MODULE_DIR)

from routines.routine_db import load_routines
from routines.routine_executor import execute_action

logger = logging.getLogger("routine_engine")
schedule_lock = threading.Lock()

# Server timezone is UTC on many hosts — we store times as IST (Asia/Kolkata).
LOCAL_TZ = ZoneInfo("Asia/Kolkata")
UTC_TZ = ZoneInfo("UTC")

WEEKDAY_MAP = {
    "monday": "monday",
    "tuesday": "tuesday",
    "wednesday": "wednesday",
    "thursday": "thursday",
    "friday": "friday",
    "saturday": "saturday",
    "sunday": "sunday",
    "daily": "daily",
    "once": "once"
}

def _ist_time_to_utc_hhmm(ist_hhmm: str):
    """
    Convert an HH:MM time string in IST -> HH:MM string in UTC.
    schedule library schedules based on server localtime (which is usually UTC in cloud).
    """
    if not ist_hhmm:
        return None
    try:
        hh, mm = ist_hhmm.split(":")
        hh = int(hh); mm = int(mm)
        now = datetime.now(UTC_TZ)
        # create a datetime today at IST time, then convert to UTC
        dt_ist = datetime(now.year, now.month, now.day, hh, mm, tzinfo=LOCAL_TZ)
        dt_utc = dt_ist.astimezone(UTC_TZ)
        return f"{dt_utc.hour:02d}:{dt_utc.minute:02d}"
    except Exception as e:
        logger.exception("Time conversion failed: %s", e)
        return ist_hhmm  # fallback

def wrap_execute(action):
    logger.info("Executing routine action now: %s", action)
    try:
        execute_action(action)
    except Exception as e:
        logger.exception("Error executing action: %s", e)

def register_routine(routine):
    t = routine.get("trigger", {})
    action = routine.get("action", {})
    value = t.get("value")
    if not value:
        logger.warning("Skipping routine with no time value: %s", routine)
        return

    freq = t.get("frequency", "once")
    logger.info("Registering routine: freq=%s time=%s action=%s", freq, value, action)

    # convert IST stored time -> UTC string for scheduling on server (if server runs in UTC)
    utc_time = _ist_time_to_utc_hhmm(value)

    if freq == "daily":
        schedule.every().day.at(utc_time).do(wrap_execute, action)
    elif freq in WEEKDAY_MAP and freq != "once":
        # e.g. schedule.every().wednesday.at(utc_time)
        getattr(schedule.every(), freq).at(utc_time).do(wrap_execute, action)
    else:
        # "once" job: schedule at utc_time today (we will not auto-remove here)
        schedule.every().day.at(utc_time).do(wrap_execute, action)

def reload_routines():
    """Clear existing jobs and load fresh routines from DB."""
    with schedule_lock:
        logger.debug("Deleting *all* jobs")
        schedule.clear()
        routines = load_routines()
        logger.info("Reloading routines: %d routines found", len(routines))
        for r in routines:
            register_routine(r)
        logger.info("[ROUTINE] Reload complete.")

def start_engine(poll_interval=1):
    """
    Start scheduler loop. This will block; spawn in a thread with daemon=True.
    """
    # initial load
    try:
        logger.exception("DEBUGGING INFO : ByPassing Routine Reloading")
        #reload_routines()
    except Exception:
        logger.exception("Initial reload failed")

    logger.info("[ROUTINE] Engine started. Waiting for schedule...")
    while True:
        try:
            schedule.run_pending()
            time.sleep(poll_interval)
        except Exception:
            logger.exception("Scheduler loop crashed — continuing.")
            time.sleep(poll_interval)