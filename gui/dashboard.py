# gui/dashboard.py
import json
import tkinter as tk
import paho.mqtt.client as mqtt

from mqtt_config import BROKER_HOST, BROKER_PORT, TOPIC_STATUS, TOPIC_ALARM, TOPIC_BUTTON


class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Parking Dashboard")

        self.lbl_parking = tk.Label(root, text="Parking: ?", font=("Arial", 18))
        self.lbl_gate = tk.Label(root, text="Gate: ?", font=("Arial", 18))
        self.lbl_level = tk.Label(root, text="Level: INFO", font=("Arial", 14))
        self.lbl_msg = tk.Label(root, text="Message: -", font=("Arial", 12), wraplength=560, justify="left")

        self.lbl_parking.pack(pady=6)
        self.lbl_gate.pack(pady=6)
        self.lbl_level.pack(pady=6)
        self.lbl_msg.pack(pady=6)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Open Gate", width=14, command=self.open_gate).grid(row=0, column=0, padx=6)
        tk.Button(btn_frame, text="Close Gate", width=14, command=self.close_gate).grid(row=0, column=1, padx=6)

        self.client = mqtt.Client(client_id="parking_gui")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.connect(BROKER_HOST, BROKER_PORT, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        client.subscribe(TOPIC_STATUS)
        client.subscribe(TOPIC_ALARM)

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode("utf-8").strip()
        if msg.topic == TOPIC_STATUS:
            try:
                data = json.loads(payload)
                occupied = bool(data.get("parking_occupied", False))
                gate_open = bool(data.get("gate_open", False))
                level = data.get("last_level", "INFO")
                message = data.get("last_message", "-")
                self.root.after(0, lambda: self.update_ui(occupied, gate_open, level, message))
            except Exception:
                pass
        elif msg.topic == TOPIC_ALARM:
            try:
                data = json.loads(payload)
                level = data.get("level", "INFO")
                message = data.get("message", "-")
                self.root.after(0, lambda: self.update_level(level, message))
            except Exception:
                pass

    def update_ui(self, occupied: bool, gate_open: bool, level: str, message: str):
        self.lbl_parking.config(text=f"Parking: {'OCCUPIED 🚗' if occupied else 'FREE 🅿️'}")
        self.lbl_gate.config(text=f"Gate: {'OPEN ✅' if gate_open else 'CLOSED ❌'}")
        self.update_level(level, message)

    def update_level(self, level: str, message: str):
        self.lbl_level.config(text=f"Level: {level}")
        self.lbl_msg.config(text=f"Message: {message}")

    def open_gate(self):
        self.client.publish(TOPIC_BUTTON, "open")
        self.update_level("INFO", "GUI sent: open")

    def close_gate(self):
        self.client.publish(TOPIC_BUTTON, "close")
        self.update_level("INFO", "GUI sent: close")


def main():
    root = tk.Tk()
    root.geometry("640x270")
    Dashboard(root)
    root.mainloop()


if __name__ == "__main__":
    main()
