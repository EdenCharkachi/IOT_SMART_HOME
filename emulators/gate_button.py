import paho.mqtt.client as mqtt
from mqtt_config import BROKER_HOST, BROKER_PORT, TOPIC_BUTTON

client = mqtt.Client("button_emulator")
client.connect(BROKER_HOST, BROKER_PORT, 60)

while True:
    cmd = input("Type open/close: ")
    if cmd in ("open","close"):
        client.publish(TOPIC_BUTTON, cmd)
