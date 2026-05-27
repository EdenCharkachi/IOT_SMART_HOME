# emulators/gate_button_emulator.py
# Producer: simulates a physical button/knob (open/close)
import paho.mqtt.client as mqtt

from mqtt_config import BROKER_HOST, BROKER_PORT, TOPIC_BUTTON

def main():
    client = mqtt.Client(client_id="gate_button_emulator")
    client.connect(BROKER_HOST, BROKER_PORT, 60)

    print("Gate Button Emulator started.")
    print("Commands: open | close | q")

    while True:
        cmd = input("> ").strip().lower()
        if cmd == "q":
            break
        if cmd in ("open", "close"):
            client.publish(TOPIC_BUTTON, cmd)
            print("Button ->", cmd)
        else:
            print("Invalid. Use open/close/q")

if __name__ == "__main__":
    main()
