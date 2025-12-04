#routine_executor.py
import time
import os
import sys

project_root = os.path.abspath("C:\\Users\\User One\\Desktop\\VORTEX-v2")
sys.path.append(project_root)

from commands.XAUTOMATION import ESPController
RoomControl(5, 'ON')


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