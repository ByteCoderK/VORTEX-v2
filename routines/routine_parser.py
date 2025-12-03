#routine_parser.py

import re
import json

ROUTINE_FILE = "data/routines.json"

def parse_routine(text: str) -> dict:
    # ======== PARSING =========
    time_match = re.search(r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)?', text, re.IGNORECASE)
    if time_match:
        hour = int(time_match.group(1))
        minute = int(time_match.group(2)) if time_match.group(2) else 0
        meridian = time_match.group(3)

        if meridian:
            if meridian.lower() == 'pm' and hour != 12:
                hour += 12
            if meridian.lower() == 'am' and hour == 12:
                hour = 0

        time_str = f"{hour:02d}:{minute:02d}"
    else:
        time_str = None

    if "every day" in text.lower():
        freq = "daily"
    elif "every monday" in text.lower():
        freq = "monday"
    elif "every tuesday" in text.lower():
        freq = "tuesday"
    else:
        freq = "once"

    if "turn on" in text.lower():
        command = "turn_on"
        device = text.lower().split("turn on")[-1].strip()
    elif "turn off" in text.lower():
        command = "turn_off"
        device = text.lower().split("turn off")[-1].strip()
    else:
        command = "unknown"
        device = "unknown"

    routine_data = {
        "trigger": {
            "type": "time",
            "value": time_str,
            "frequency": freq
        },
        "action": {
            "device": device,
            "command": command
        }
    }

    # ======== APPEND TO JSON =========
    try:
        with open(ROUTINE_FILE, "r") as f:
            existing = json.load(f)
    except:
        existing = []  # if file empty/corrupt we create list but DO NOT create file here

    existing.append(routine_data)

    with open(ROUTINE_FILE, "w") as f:
        json.dump(existing, f, indent=4)

    return routine_data