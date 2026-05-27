import time, random
import paho.mqtt.client as mqtt
from mqtt_config import BROKER_HOST, BROKER_PORT, TOPIC_SENSOR

client = mqtt.Client("sensor_emulator")
client.connect(BROKER_HOST, BROKER_PORT, 60)

state = "free"
while True:
    if random.random() < 0.4:
        state = "occupied" if state == "free" else "free"
        client.publish(TOPIC_SENSOR, state)
        print("Sensor:", state)
    time.sleep(3)
