from commands.XAUTOMATION import ESPController
import os
DEVICE_MAP = {
    "light": 1,
    "wind": 2,
    "ambient": 3,
    "socket": 4
}

def required_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        raise RuntimeError(f"Missing env var: {name}")
    return value

# ---------------- ESP Controller ----------------
broker = required_env('broker')
username = required_env('username')
password = required_env('password')
topic_cmd = required_env('topic_cmd_2')
topic_feedback = required_env('topic_feedback_2')

# INIT MQTT CONTROLLER
esp = ESPController(
    broker=broker,
    port=8883,
    username=username,
    password=password,
    topic_cmd=topic_cmd,
    topic_feedback=topic_feedback
)

def control_device(device_name, state):
    relay = DEVICE_MAP.get(device_name.lower())
    if not relay:
        raise ValueError(f"Unknown device: {device_name}")
    esp.RoomControl(relay, state)