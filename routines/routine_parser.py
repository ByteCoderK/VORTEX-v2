import re
import json

ROUTINE_FILE = "data/routines.json"

DEVICE_MAP = {
    "light": 1,
    "wind": 2,
    "ambient": 3,
    "socket": 4
}

def parse_routine(text: str) -> dict:
    # ======== PARSE TIME =========
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

    # ======== PARSE FREQUENCY =========
    lower = text.lower()
    if "every day" in lower:
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

    # ======== PARSE ACTION =========
    # ON/OFF
    if "turn on" in lower:
        state = "ON"
        device_name = lower.split("turn on")[-1].strip()
    elif "turn off" in lower:
        state = "OFF"
        device_name = lower.split("turn off")[-1].strip()
    else:
        state = None
        device_name = None

    # Map device to relay num
    relay = None
    if device_name:
        for key in DEVICE_MAP:
            if key in device_name:
                relay = DEVICE_MAP[key]
                break

    # ======== FINAL ACTION STRUCTURE (MATCHES EXECUTOR) ========
    action = {
        "type": "device",
        "relay": relay,
        "state": state
    }

    # ======== BUILD ROUTINE DICT =========
    routine_data = {
        "trigger": {
            "type": "time",
            "value": time_str,
            "frequency": freq
        },
        "action": action
    }

    # ======== SAVE TO JSON =========
    try:
        with open(ROUTINE_FILE, "r") as f:
            existing = json.load(f)
    except:
        existing = []  # File exists but empty or corrupt

    existing.append(routine_data)

    with open(ROUTINE_FILE, "w") as f:
        json.dump(existing, f, indent=4)

    return routine_data