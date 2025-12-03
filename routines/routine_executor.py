#routine_executor.py

from commands.XAUTOMATION import *
import time

def execute_action(action):
    """
    action example:
    {
        "type": "device",
        "relay": 1,
        "state": "ON"
    }
    """

    if action["type"] == "device":
        relay = action.get("relay")
        state = action.get("state")
        RoomControl(relay, state)

    elif action["type"] == "delay":
        time.sleep(action["seconds"])

    else:
        print(f"[ROUTINE] Unknown action type: {action}")