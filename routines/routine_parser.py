# routines/routine_parser.py
import re
from datetime import datetime

DEVICE_MAP = ["light", "wind", "ambient", "socket"]  # names only

def parse_routine(text: str):
    text = text.lower()
    
    # --- Time parsing ---
    time_str = None
    m = re.search(r'(\d{1,2}):(\d{2})\s*(am|pm)?', text)
    if m:
        hour, minute = int(m.group(1)), int(m.group(2))
        mer = m.group(3)
        if mer:
            if mer == "pm" and hour != 12: hour += 12
            if mer == "am" and hour == 12: hour = 0
        time_str = f"{hour:02d}:{minute:02d}"
    if not time_str:
        raise ValueError("Could not parse time")

    # --- Frequency ---
    freq = "once"
    weekdays = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
    for day in weekdays:
        if f"every {day}" in text:
            freq = day
            break
    if "every day" in text:
        freq = "daily"

    # --- Action ---
    state = None
    for s in ["turn on","turn off"]:
        if s in text:
            state = "ON" if "on" in s else "OFF"
            break
    if not state:
        raise ValueError("No action detected")

    device = None
    for d in DEVICE_MAP:
        if d in text:
            device = d
            break
    if not device:
        raise ValueError("No valid device detected")

    return {
        "trigger": {"type": "time", "value": time_str, "frequency": freq},
        "action": {"type": "device", "device": device, "state": state}
    }