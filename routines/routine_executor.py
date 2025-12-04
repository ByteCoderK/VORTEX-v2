#routine_executor.py
import time
import os
import sys

project_root = os.path.abspath("C:\\Users\\User One\\Desktop\\VORTEX-v2")
sys.path.append(project_root)

from commands.XAUTOMATION import ESPController

# Create the controller object
controller = ESPController(
    broker="yourbroker.hivemq.cloud",
    port=8883,
    username="xxxx",
    password="xxxx",
    topic_cmd="your/cmd/topic",
    topic_feedback="your/feedback/topic"
)

# Now call the method correctly
controller.RoomControl(5, 'ON')



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
        controller.RoomControl(relay, state)

    elif action["type"] == "delay":
        time.sleep(action["seconds"])

    else:
        print(f"[ROUTINE] Unknown action type: {action}")