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
    lower = text.lower()

    # ==========================
    #  SMART TIME PARSING
    # ==========================
    time_str = None

    # Priority 1: HH:MM AM/PM
    m = re.search(r'\b(\d{1,2}):(\d{2})\s*(am|pm)\b', lower)
    if m:
        hour = int(m.group(1))
        minute = int(m.group(2))
        mer = m.group(3)

        if mer == "pm" and hour != 12:
            hour += 12
        if mer == "am" and hour == 12:
            hour = 0

        time_str = f"{hour:02d}:{minute:02d}"

    # Priority 2: HH AM/PM
    if not time_str:
        m = re.search(r'\b(\d{1,2})\s*(am|pm)\b', lower)
        if m:
            hour = int(m.group(1))
            mer = m.group(2)

            if mer == "pm" and hour != 12:
                hour += 12
            if mer == "am" and hour == 12:
                hour = 0

            time_str = f"{hour:02d}:00"

    # Priority 3: HH:MM 24-hour
    if not time_str:
        m = re.search(r'\b(\d{1,2}):(\d{2})\b', lower)
        if m:
            hour = int(m.group(1))
            minute = int(m.group(2))
            if 0 <= hour <= 23:
                time_str = f"{hour:02d}:{minute:02d}"

    # Priority 4: Single hour
    if not time_str:
        m = re.search(r'\b(\d{1,2})\b', lower)
        if m:
            hour = int(m.group(1))
            if 0 <= hour <= 23:
                time_str = f"{hour:02d}:00"

    # ==========================
    #  SMART FREQUENCY PARSING
    # ==========================
    weekdays = [
        "monday","tuesday","wednesday",
        "thursday","friday","saturday","sunday"
    ]
    freq = "once"
    for day in weekdays:
        if day in lower:
            freq = day
            break
    if "every day" in lower:
        freq = "daily"

    # ==========================
    #  SMART ACTION PARSING
    # ==========================
    state = None
    if "turn on" in lower:
        state = "ON"
        device_part = lower.split("turn on")[-1]
    elif "turn off" in lower:
        state = "OFF"
        device_part = lower.split("turn off")[-1]
    else:
        device_part = ""

    relay = None
    for name, num in DEVICE_MAP.items():
        if name in device_part:
            relay = num
            break

    action = {
        "type": "device",
        "relay": relay,
        "state": state
    }

    routine_data = {
        "trigger": {
            "type": "time",
            "value": time_str,
            "frequency": freq
        },
        "action": action
    }

    # ==========================
    #  SAVE TO JSON
    # ==========================
    try:
        with open(ROUTINE_FILE, "r") as f:
            existing = json.load(f)
            if not isinstance(existing, list):
                existing = []
    except:
        existing = []

    existing.append(routine_data)

    with open(ROUTINE_FILE, "w") as f:
        json.dump(existing, f, indent=4)

    return routine_data