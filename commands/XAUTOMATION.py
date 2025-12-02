import paho.mqtt.client as mqtt
import time

class ESPController:
    def __init__(self,
                 broker: str,
                 port: int,
                 username: str,
                 password: str,
                 topic_cmd: str,
                 topic_feedback: str):

        self.broker = broker
        self.port = port
        self.topic_cmd = topic_cmd
        self.topic_feedback = topic_feedback

        self.client = mqtt.Client()
        self.client.username_pw_set(username, password)
        self.client.tls_set()

        # Bind callbacks
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

        # Connect
        self.client.connect(self.broker, self.port)
        self.client.loop_start()
        time.sleep(1)

    # ---------- Callbacks ----------
    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("✔ Connected to HiveMQ Cloud")
            client.subscribe(self.topic_feedback)
        else:
            print(f"❌ Failed to connect, rc={rc}")

    def _on_message(self, client, userdata, msg):
        print(f"📨 ESP Feedback → {msg.topic}: {msg.payload.decode()}")

    # ---------- Public Method ----------
    def RoomControl(self, relay: int, state: str):
        """
        relay: 1–4
        state: "ON" or "OFF"
        """
        command_map = {
            (1, "ON"): "1", (1, "OFF"): "2",
            (2, "ON"): "3", (2, "OFF"): "4",
            (3, "ON"): "5", (3, "OFF"): "6",
            (4, "ON"): "7", (4, "OFF"): "8",
        }

        cmd = command_map.get((relay, state.upper()))
        if not cmd:
            print("❌ Invalid relay/state")
            return

        result = self.client.publish(self.topic_cmd, cmd)

        if result[0] == 0:
            print(f"📤 Sent → Relay {relay} {state} (cmd={cmd})")
        else:
            print("❌ Failed to publish command")
