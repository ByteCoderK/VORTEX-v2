# routine_parser.py

import re
from datetime import datetime

def parse_routine(text: str) -> dict:
    """
    Parses user-defined routines from plain text.
    Example:
      "Every day at 7AM turn on the bedroom light"
      "At 9pm turn off fan"
      "Every Monday at 6 do a system check"
    Returns:
      {
        "trigger": {
            "type": "time",
            "value": "07:00",
            "frequency": "daily"
        },
        "action": {
            "device": "bedroom light",
            "command": "turn_on"
        }
      }
    """

    # VERY BASIC IMPLEMENTATION — good enough for now

    # 1) TIME
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

    # 2) FREQUENCY
    if "every day" in text.lower():
        freq = "daily"
    elif "every monday" in text.lower():
        freq = "monday"
    elif "every tuesday" in text.lower():
        freq = "tuesday"
    else:
        freq = "once"

    # 3) ACTION
    if "turn on" in text.lower():
        command = "turn_on"
        device = text.lower().split("turn on")[-1].strip()
    elif "turn off" in text.lower():
        command = "turn_off"
        device = text.lower().split("turn off")[-1].strip()
    else:
        command = "unknown"
        device = "unknown"

    return {
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