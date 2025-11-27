import paho.mqtt.client as mqtt
import time

# HiveMQ credentials and broker
broker = "c4f73c571367445282f1ae6cd0e5e0ce.s1.eu.hivemq.cloud"
port = 8883
username = "VORTEX"
password = "ffc-5DF0FSD9AS8-e./';..ls./'lp./';..l-iucfbYwaSDewiaubv-lliot"

topic_sub = "vortex/feedback"

# Callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("\u2705 Connected to HiveMQ Cloud")
        client.subscribe(topic_sub)
    else:
        print(f"\u274C Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    print(f"📨 Message from {msg.topic}: {msg.payload.decode()}")

# MQTT client setup
client = mqtt.Client()
client.username_pw_set(username, password)
client.tls_set()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, port)
client.loop_start()
time.sleep(2)

# Relay control command sender
def RoomControl(relay_number: int, state: str):
    """
    relay_number: 1 to 4
    state: "ON" or "OFF"
    """
    command_map = {
        (1, "ON"): "1",
        (1, "OFF"): "2",
        (2, "ON"): "3",
        (2, "OFF"): "4",
        (3, "ON"): "5",
        (3, "OFF"): "6",
        (4, "ON"): "7",
        (4, "OFF"): "8",
    }

    command = command_map.get((relay_number, state.upper()))
    if command:
        result = client.publish("vortex/relay1", command)
        status = result[0]
        if status == 0:
            print(f"📤 Sent command '{command}' for Relay {relay_number} ({state})")
            return f"📤 {relay_number} is now {state}"
        else:
            print(f"\u274C Failed to send command to Relay {relay_number}")
    else:
        print("\u274C Invalid relay number or state")

