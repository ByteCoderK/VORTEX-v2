#routine_executor.py
import time
from routines.devices import control_device

def execute_action(action):
    action_type = action.get("type")
    if action_type == "device":
        control_device(action["device"], action["state"])
    elif action_type == "delay":
        time.sleep(action.get("seconds", 1))
    else:
        raise ValueError(f"Unknown action type: {action_type}")