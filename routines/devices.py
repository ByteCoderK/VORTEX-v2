#devices.py
# Map of device names to relays
DEVICE_MAP = {
    "light": 1,
    "wind": 2,
    "ambient": 3,
    "socket": 4
}

# Import your ESPController from XAutomation here
from commands.XAUTOMATION import ESPController

# Single ESP instance, initialized once
esp = ESPController(
    broker="broker.hivemq.com",
    port=8883,
    username="user",
    password="pass",
    topic_cmd="home/cmd",
    topic_feedback="home/feedback"
)

def control_device(device_name, state):
    relay = DEVICE_MAP.get(device_name.lower())
    if not relay:
        raise ValueError(f"Unknown device: {device_name}")
    esp.RoomControl(relay, state)