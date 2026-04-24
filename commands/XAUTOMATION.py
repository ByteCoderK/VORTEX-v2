#XAutomation.py
import logging
import time

import paho.mqtt.client as mqtt

logger = logging.getLogger("vortex.xautomation")


class ESPController:
    def __init__(
        self,
        broker: str,
        port: int,
        username: str,
        password: str,
        topic_cmd: str,
        topic_feedback: str,
    ):
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
        logger.info("Connecting to MQTT broker %s:%s", self.broker, self.port)
        self.client.connect(self.broker, self.port)
        self.client.loop_start()
        time.sleep(1)

    # ---------- Callbacks ----------
    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info("Connected to HiveMQ Cloud")
            print("Connected to HiveMQ Cloud")
            client.subscribe(self.topic_feedback)
        else:
            logger.error("Failed to connect to MQTT broker rc=%s", rc)
            print(f"Failed to connect, rc={rc}")

    def _on_message(self, client, userdata, msg):
        payload = msg.payload.decode()
        logger.info("ESP feedback topic=%s payload=%s", msg.topic, payload)
        print(f"ESP Feedback -> {msg.topic}: {payload}")

    # ---------- Public Method ----------
    def RoomControl(self, relay: int, state: str):
        """
        relay: 1-4
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

        cmd = command_map.get((relay, state.upper()))
        if not cmd:
            logger.warning("Invalid relay/state combination relay=%s state=%s", relay, state)
            print("Invalid relay/state")
            return

        logger.info("Publishing MQTT command relay=%s state=%s cmd=%s", relay, state, cmd)
        result = self.client.publish(self.topic_cmd, cmd)

        if result[0] == 0:
            logger.info("MQTT command published successfully")
            print(f"Sent -> Relay {relay} {state} (cmd={cmd})")
        else:
            logger.error("Failed to publish MQTT command")
            print("Failed to publish command")
