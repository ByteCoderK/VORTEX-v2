
# devices.py
from commands.XAUTOMATION import ESPController

DEVICE_MAP = {
    "light": 1,
    "wind": 2,
    "ambient": 3,
    "socket": 4
}

# ---------------- ESP Controller ----------------
esp = ESPController(
    broker="c4f73c571367445282f1ae6cd0e5e0ce.s1.eu.hivemq.cloud",
    port=8883,
    username="VORTEX",
    password="ffc-5DF0FSD9AS8-e./';..ls./'lp./';..l-iucfbYwaSDewiaubv-lliot",
    topic_cmd="home/cmd",         # You can change to your actual topic
    topic_feedback="home/feedback" # Your feedback topic
)

def control_device(device_name, state):
    relay = DEVICE_MAP.get(device_name.lower())
    if not relay:
        raise ValueError(f"Unknown device: {device_name}")
    esp.RoomControl(relay, state)