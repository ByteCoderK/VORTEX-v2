import paho.mqtt.client as mqtt
import time

# HiveMQ credentials and broker
broker = "c4f73c571367445282f1ae6cd0e5e0ce.s1.eu.hivemq.cloud"
port = 8883
username = "VORTEX"
password = "ffc-5DF0FSD9AS8-e./';..ls./'lp./';..l-iucfbYwaSDewiaubv-lliot"

# Topics
topic_pub = "vortex/relay1"
topic_sub = "vortex/feedback"

# Callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to HiveMQ Cloud")
        client.subscribe(topic_sub)
    else:
        print(f"❌ Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    print(f"📨 Message from {msg.topic}: {msg.payload.decode()}")

# MQTT client setup
client = mqtt.Client()
client.username_pw_set(username, password)
client.tls_set()
client.on_connect = on_connect
client.on_message = on_message
# Connect and start loop
client.connect(broker, port)
client.loop_start()

# Give it time to connect
time.sleep(2)

# Send command to relay
result = client.publish(topic_pub, '2')
status = result[0]
if status == 0:
    print(f"📤 Sent '1' to topic {topic_pub}")
else:
    print(f"❌ Failed to send message to topic {topic_pub}")

# Optional: keep running to listen for messages
time.sleep(10)
client.loop_stop()
client.disconnect()
