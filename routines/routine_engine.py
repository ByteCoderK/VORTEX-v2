import os
import sys
import schedule
import time
import logging
import threading
import re
from datetime import datetime
from zoneinfo import ZoneInfo

MODULE_DIR = os.path.dirname(__file__)
sys.path.append(MODULE_DIR)

from routines.routine_db import load_routines
from routines.routine_executor import execute_action

logger = logging.getLogger("routine_engine")
schedule_lock = threading.Lock()

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

_HHMM_RE = re.compile(r'^[0-2]\d:[0-5]\d$')


def _validate_hhmm(hhmm: str) -> bool:
    """Return True if hhmm is valid HH:MM (24h)."""
    if not hhmm or not isinstance(hhmm, str):
        return False
    return bool(_HHMM_RE.match(hhmm))


def _ist_time_to_utc_hhmm(ist_hhmm: str) -> str | None:
    """
    Convert an HH:MM time string in IST -> HH:MM string in UTC.
    schedule library schedules based on server localtime (which is usually UTC in cloud).
    Returns normalized "HH:MM" or None on failure.
    """
    if not ist_hhmm:
        return None
    try:
        parts = ist_hhmm.split(":")
        if len(parts) != 2:
            logger.warning("Bad IST time format (not HH:MM): %s", ist_hhmm)
            return None
        hh = int(parts[0])
        mm = int(parts[1])
        if not (0 <= hh <= 23 and 0 <= mm <= 59):
            logger.warning("IST time out of range: %s", ist_hhmm)
            return None

        now_utc = datetime.now(UTC_TZ)
        dt_ist = datetime(now_utc.year, now_utc.month, now_utc.day, hh, mm, tzinfo=LOCAL_TZ)
        dt_utc = dt_ist.astimezone(UTC_TZ)
        utc_str = f"{dt_utc.hour:02d}:{dt_utc.minute:02d}"
        logger.debug("routine_engine: IST=%s -> UTC=%s", ist_hhmm, utc_str)
        return utc_str
    except Exception as e:
        logger.exception("Time conversion failed for %s: %s", ist_hhmm, e)
        return None


def wrap_execute(action):
    logger.info("Executing routine action now: %s", action)
    try:
        execute_action(action)
    except Exception as e:
        logger.exception("Error executing action: %s", e)


def register_routine(routine):
    """
    Register a single routine with the scheduler.
    Routine expected shape:
      {
        "trigger": {"type": "time", "value": "HH:MM", "frequency": "monday|daily|once|..."},
        "action": {...}
      }
    """
    try:
        t = routine.get("trigger", {})
        action = routine.get("action", {})
        value = t.get("value")
        if not value:
            logger.warning("Skipping routine with no time value: %s", routine)
            return

        freq = (t.get("frequency") or "once").lower()
        logger.info("Registering routine: freq=%s time=%s action=%s", freq, value, action)

        utc_time = _ist_time_to_utc_hhmm(value)
        if not utc_time:
            logger.warning("Skipping routine due to invalid time conversion: %s", value)
            return

        if not _validate_hhmm(utc_time):
            logger.warning("Skipping routine; invalid HH:MM after conversion: %s", utc_time)
            return

        try:
            if freq == "daily":
                schedule.every().day.at(utc_time).do(wrap_execute, action)
            elif freq in WEEKDAY_MAP and freq != "once":
                getattr(schedule.every(), freq).at(utc_time).do(wrap_execute, action)
            else:
                schedule.every().day.at(utc_time).do(wrap_execute, action)
        except Exception as e:
            logger.exception("Failed to schedule routine (freq=%s time=%s): %s", freq, utc_time, e)
            return

        logger.debug("Registered job count: %d", len(schedule.get_jobs()))
    except Exception:
        logger.exception("Unhandled error while registering routine: %s", routine)


def reload_routines():
    with schedule_lock:
        try:
            logger.debug("Deleting *all* jobs")
            schedule.clear()
            routines = load_routines()
            logger.info("Reloading routines: %d routines found", len(routines))
            for r in routines:
                register_routine(r)
            logger.info("[ROUTINE] Reload complete. Jobs registered: %d", len(schedule.get_jobs()))
        except Exception:
            logger.exception("Failed reloading routines")


def start_engine(poll_interval=1):
    try:
        reload_routines()
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