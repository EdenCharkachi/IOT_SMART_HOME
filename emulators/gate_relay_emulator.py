# emulators/gate_relay_emulator.py
# Actuator emulator: listens for gate commands and publishes ack (opened/closed)
import time
import paho.mqtt.client as mqtt

from mqtt_config import BROKER_HOST, BROKER_PORT, TOPIC_GATE_CMD, TOPIC_GATE_ACK

class GateRelayEmulator:
    def __init__(self):
        self.state = "closed"  # opened/closed
        self.client = mqtt.Client(client_id="gate_relay_emulator")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        print("Gate Relay Emulator connected. Listening for commands...")
        client.subscribe(TOPIC_GATE_CMD)

    def on_message(self, client, userdata, msg):
        cmd = msg.payload.decode("utf-8").strip().lower()
        if cmd not in ("open", "close"):
            print("Unknown command:", cmd)
            return

        # Simulate relay action time
        time.sleep(0.5)

        if cmd == "open":
            self.state = "opened"
            client.publish(TOPIC_GATE_ACK, "opened")
            print("Relay -> opened (ack sent)")
        else:
            self.state = "closed"
            client.publish(TOPIC_GATE_ACK, "closed")
            print("Relay -> closed (ack sent)")

    def run(self):
        self.client.connect(BROKER_HOST, BROKER_PORT, 60)
        self.client.loop_forever()

if __name__ == "__main__":
    GateRelayEmulator().run()
