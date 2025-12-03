# routines/routine_parser.py
import re
import json
import os
from routines.routine_engine import reload_routines


MODULE_DIR = os.path.dirname(__file__)
ROUTINE_FILE = os.path.join(MODULE_DIR, "data", "routines.json")

DEVICE_MAP = {
    "light": 1,
    "wind": 2,
    "ambient": 3,
    "socket": 4
}

def parse_routine(text: str) -> dict:
    lower = text.lower()
    # --- time parsing (your smarter version) ---
    time_str = None
    m = re.search(r'\b(\d{1,2}):(\d{2})\s*(am|pm)\b', lower)
    if m:
        hour = int(m.group(1)); minute = int(m.group(2)); mer = m.group(3)
        if mer == "pm" and hour != 12: hour += 12
        if mer == "am" and hour == 12: hour = 0
        time_str = f"{hour:02d}:{minute:02d}"
    if not time_str:
        m = re.search(r'\b(\d{1,2})\s*(am|pm)\b', lower)
        if m:
            hour = int(m.group(1)); mer = m.group(2)
            if mer == "pm" and hour != 12: hour += 12
            if mer == "am" and hour == 12: hour = 0
            time_str = f"{hour:02d}:00"
    if not time_str:
        m = re.search(r'\b([01]?\d|2[0-3]):([0-5]\d)\b', lower)
        if m:
            hour = int(m.group(1)); minute = int(m.group(2))
            time_str = f"{hour:02d}:{minute:02d}"

    # frequency
    if "every day" in lower: freq = "daily"
    elif "every monday" in lower: freq = "monday"
    elif "every tuesday" in lower: freq = "tuesday"
    elif "every wednesday" in lower: freq = "wednesday"
    elif "every thursday" in lower: freq = "thursday"
    elif "every friday" in lower: freq = "friday"
    elif "every saturday" in lower: freq = "saturday"
    elif "every sunday" in lower: freq = "sunday"
    else: freq = "once"

    # action
    if "turn on" in lower:
        state = "ON"
        device_name = lower.split("turn on")[-1].strip()
    elif "turn off" in lower:
        state = "OFF"
        device_name = lower.split("turn off")[-1].strip()
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

    # ======== SAVE TO JSON (same place as routine_db) =========
    try:
        # load existing safely
        if os.path.exists(ROUTINE_FILE):
            with open(ROUTINE_FILE, "r") as f:
                existing = json.load(f) or []
        else:
            existing = []
    except Exception:
        existing = []

    existing.append(routine_data)
    with open(ROUTINE_FILE, "w") as f:
        json.dump(existing, f, indent=4)

    reload_routines()
    return routine_data