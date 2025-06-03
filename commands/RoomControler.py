import paho.mqtt.client as mqtt

# Your HiveMQ credentials
broker = "c4f73c571367445282f1ae6cd0e5e0ce.s1.eu.hivemq.cloud"
port = 8883
username = "VORTEX"
password = "ffc-5DF0FSD9AS8-e./';..ls./'lp./';..l-iucfbYwaSDewiaubv-lliot"

topic_pub = "vortex/relay1"
topic_sub = "vortex/feedback"  # optional

# Callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to HiveMQ Cloud!")
        client.subscribe(topic_sub)
    else:
        print(f"Connection failed with code {rc}")

def on_message(client, userdata, msg):
    print(f"Message from {msg.topic}: {msg.payload.decode()}")

# MQTT setup
client = mqtt.Client()
client.username_pw_set(username, password)
client.tls_set()  # Use TLS
client.on_connect = on_connect
client.on_message = on_message

# Connect & loop
client.connect(broker, port)
client.loop_start()

# Send command
client.publish(topic_pub, "1")  # Trigger relay ON
