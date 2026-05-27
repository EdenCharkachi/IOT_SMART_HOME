# emulators/parking_sensor_emulator.py
# Data producer: simulates a parking occupancy sensor (occupied/free)
import time
import random
import paho.mqtt.client as mqtt

from mqtt_config import BROKER_HOST, BROKER_PORT, TOPIC_SENSOR

def main():
    client = mqtt.Client(client_id="parking_sensor_emulator")
    client.connect(BROKER_HOST, BROKER_PORT, 60)

    state = "free"
    print("Parking Sensor Emulator started (publishes: occupied/free). CTRL+C to stop.")

    while True:
        if random.random() < 0.35:
            state = "occupied" if state == "free" else "free"
            client.publish(TOPIC_SENSOR, state)
            print("Sensor ->", state)
        time.sleep(3)

if __name__ == "__main__":
    main()
