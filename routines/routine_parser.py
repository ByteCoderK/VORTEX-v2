# routines/routine_parser.py
import re
import logging
from datetime import datetime
from routines.routine_db import add_routine

logger = logging.getLogger("routine_parser")

DEVICE_MAP = {
    "light": 1,
    "wind": 2,
    "ambient": 3,
    "socket": 4
}

def _normalize_time_from_matches(hour: int, minute: int, meridian: str | None) -> str:
    """Return HH:MM in 24-hour format (string)."""
    if meridian:
        meridian = meridian.lower()
        if meridian == "pm" and hour != 12:
            hour += 12
        if meridian == "am" and hour == 12:
            hour = 0
    # clamp hour/minute safely
    hour = max(0, min(23, hour))
    minute = max(0, min(59, minute))
    return f"{hour:02d}:{minute:02d}"

def parse_routine(text: str) -> dict:
    """
    Parse a user text into a routine dict, persist it, and return the saved routine.
    The returned dict matches the format used by the engine:
      {
        "trigger": {"type": "time", "value": "HH:MM", "frequency": "..."},
        "action": {"type":"device","relay":N,"state":"ON"/"OFF"}
      }
    If time parsing fails, "value" will be None (engine will skip it).
    """
    lower = (text or "").lower()

    # --- TIME PARSING (supports "7", "7am", "7:30 pm", "19:05") ---
    time_str = None

    # 1) explicit hh:mm am/pm e.g. "8:15 pm"
    m = re.search(r'\b([0-1]?\d|2[0-3]):([0-5]\d)\s*(am|pm)\b', lower)
    if m:
        hour = int(m.group(1)); minute = int(m.group(2)); mer = m.group(3)
        time_str = _normalize_time_from_matches(hour, minute, mer)

    # 2) hh:mm 24-hour e.g. "20:05"
    if not time_str:
        m = re.search(r'\b([01]?\d|2[0-3]):([0-5]\d)\b', lower)
        if m:
            hour = int(m.group(1)); minute = int(m.group(2))
            time_str = _normalize_time_from_matches(hour, minute, None)

    # 3) single hour with am/pm e.g. "8 pm" -> "20:00"
    if not time_str:
        m = re.search(r'\b(\d{1,2})\s*(am|pm)\b', lower)
        if m:
            hour = int(m.group(1)); mer = m.group(2)
            time_str = _normalize_time_from_matches(hour, 0, mer)

    # Frequency
    if "every day" in lower or "daily" in lower:
        freq = "daily"
    elif "every monday" in lower:
        freq = "monday"
    elif "every tuesday" in lower:
        freq = "tuesday"
    elif "every wednesday" in lower:
        freq = "wednesday"
    elif "every thursday" in lower:
        freq = "thursday"
    elif "every friday" in lower:
        freq = "friday"
    elif "every saturday" in lower:
        freq = "saturday"
    elif "every sunday" in lower:
        freq = "sunday"
    else:
        # If the user mentions a weekday explicitly like "on Wednesday" but not "every",
        # attempt to detect it:
        if "monday" in lower:
            freq = "monday"
        elif "tuesday" in lower:
            freq = "tuesday"
        elif "wednesday" in lower:
            freq = "wednesday"
        elif "thursday" in lower:
            freq = "thursday"
        elif "friday" in lower:
            freq = "friday"
        elif "saturday" in lower:
            freq = "saturday"
        elif "sunday" in lower:
            freq = "sunday"
        else:
            freq = "once"

    # Action parsing (turn on/off + device mapping)
    if "turn on" in lower:
        state = "ON"
        device_name = lower.split("turn on", 1)[-1].strip()
    elif "turn off" in lower:
        state = "OFF"
        device_name = lower.split("turn off", 1)[-1].strip()
    else:
        state = None
        device_name = None

    relay = None
    if device_name:
        for key in DEVICE_MAP:
            if key in device_name:
                relay = DEVICE_MAP[key]
                break

    action = {
        "type": "device",
        "relay": relay,
        "state": state
    }

    routine_data = {
        "trigger": {"type": "time", "value": time_str, "frequency": freq},
        "action": action
    }

    # persist via DB helper (also triggers reload if engine present)
    try:
        add_routine(routine_data)
    except Exception:
        logger.exception("Failed to add routine via DB; returning routine_data without saving")

    return routine_data