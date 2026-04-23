# routines/routine_parser.py
import re
import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo

MODULE_DIR = os.path.dirname(__file__)
ROUTINE_FILE = os.path.join(MODULE_DIR, "data", "routines.json")
DEVICE_MAP = {
    "light": 1,
    "wind": 2,
    "fan": 2,
    "ambient": 3,
    "socket": 4,
    "plug": 4
}

def _normalize_time_from_matches(hour:int, minute:int, meridian:str|None):
    """Convert hour/minute + am/pm into 24h HH:MM string (IST stored)."""
    if meridian:
        mer = meridian.lower()
        if mer == "pm" and hour != 12:
            hour += 12
        if mer == "am" and hour == 12:
            hour = 0
    return f"{hour:02d}:{minute:02d}"

def parse_routine(text: str) -> dict:
    lower = text.lower().strip()

    time_str = None
    m = re.search(r'\b(\d{1,2}):(\d{2})\s*(am|pm)\b', lower)          # 12-hour with minutes
    if m:
        time_str = _normalize_time_from_matches(int(m.group(1)), int(m.group(2)), m.group(3))
    if not time_str:
        m = re.search(r'\b(\d{1,2})\s*(am|pm)\b', lower)              # 12-hour whole hour
        if m:
            time_str = _normalize_time_from_matches(int(m.group(1)), 0, m.group(2))
    if not time_str:
        m = re.search(r'\b([01]?\d|2[0-3]):([0-5]\d)\b', lower)       # 24-hour HH:MM
        if m:
            time_str = f"{int(m.group(1)):02d}:{int(m.group(2)):02d}"

    # 2) FREQUENCY
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
        freq = "once"

    # 3) ACTION parsing (turn on / turn off)
    if "turn on" in lower:
        state = "ON"
        device_name = lower.split("turn on")[-1].strip()
    elif "turn off" in lower:
        state = "OFF"
        device_name = lower.split("turn off")[-1].strip()
    else:
        # fallback: simple tokens
        state = None
        device_name = None
        for token in ("turn", "on", "off"):
            if token in lower:
                pass

    # map device text -> relay number
    relay = None
    if device_name:
        for k,v in DEVICE_MAP.items():
            if k in device_name:
                relay = v
                break

    action = {
        "type": "device",
        "device": device_name,
        "relay": relay,
        "state": state
    }

    routine_data = {
        "trigger": {"type": "time", "value": time_str, "frequency": freq},
        "action": action
    }

    try:
        os.makedirs(os.path.dirname(ROUTINE_FILE), exist_ok=True)
        if os.path.exists(ROUTINE_FILE):
            with open(ROUTINE_FILE, "r") as f:
                existing = json.load(f) or []
        else:
            existing = []
    except Exception:
        existing = []

    existing.append(routine_data)
    try:
        with open(ROUTINE_FILE, "w") as f:
            json.dump(existing, f, indent=4)
    except Exception:
        pass

    return routine_data