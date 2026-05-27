# manager.py
import json
import sqlite3
import time
from pathlib import Path

import paho.mqtt.client as mqtt

from mqtt_config import (
    BROKER_HOST, BROKER_PORT,
    TOPIC_SENSOR, TOPIC_BUTTON,
    TOPIC_GATE_CMD, TOPIC_GATE_ACK,
    TOPIC_STATUS, TOPIC_ALARM
)

DB_PATH = Path(__file__).resolve().parent / "db" / "parking.db"


class ParkingManager:
    """
    Data Manager App:
    - Collects messages from MQTT broker
    - Writes events + snapshots to local SQLite DB
    - Processes rules and sends Warning/Alarm messages
    - Sends commands to gate actuator (relay emulator)
    """

    def __init__(self):
        self.parking_occupied = False
        self.gate_open = False

        self.last_level = "INFO"
        self.last_message = "System started"

        self.client = mqtt.Client(client_id="parking_manager")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    # ---------- DB helpers ----------
    def _db(self, query, params=()):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        conn.close()

    def log_event(self, source: str, topic: str, payload: str):
        self._db(
            "INSERT INTO events(source, topic, payload) VALUES (?,?,?)",
            (source, topic, payload)
        )

    def log_snapshot(self):
        self._db(
            "INSERT INTO state_snapshots(parking_occupied, gate_open, last_level, last_message) VALUES (?,?,?,?)",
            (1 if self.parking_occupied else 0, 1 if self.gate_open else 0, self.last_level, self.last_message)
        )

    def log_alert(self, level: str, message: str):
        self._db(
            "INSERT INTO alerts(level, message) VALUES (?,?)",
            (level, message)
        )

    # ---------- MQTT publish ----------
    def publish_status(self):
        status = {
            "parking_occupied": self.parking_occupied,
            "gate_open": self.gate_open,
            "last_level": self.last_level,
            "last_message": self.last_message,
            "ts": int(time.time())
        }
        # retained so GUI gets latest state immediately
        self.client.publish(TOPIC_STATUS, json.dumps(status), qos=0, retain=True)
        self.log_snapshot()

    def publish_alert(self, level: str, message: str):
        alert = {"level": level, "message": message, "ts": int(time.time())}
        self.client.publish(TOPIC_ALARM, json.dumps(alert), qos=0, retain=False)
        self.log_alert(level, message)

        # Also store last alert inside STATUS
        self.last_level = level
        self.last_message = message
        self.publish_status()

    def send_gate_command(self, cmd: str):
        # cmd: "open" / "close"
        self.client.publish(TOPIC_GATE_CMD, cmd, qos=0, retain=False)
        self.log_event("manager", TOPIC_GATE_CMD, cmd)

    # ---------- Rules ----------
    def handle_sensor(self, payload: str):
        if payload == "occupied":
            self.parking_occupied = True
        elif payload == "free":
            self.parking_occupied = False
        else:
            self.publish_alert("WARNING", f"Unknown sensor payload: {payload}")
            return

        # Rule: if car arrived and gate is open => close gate for safety
        if self.parking_occupied and self.gate_open:
            self.gate_open = False
            self.send_gate_command("close")
            self.publish_alert("WARNING", "Parking became OCCUPIED -> closing gate")
        else:
            self.publish_status()

    def handle_button(self, payload: str):
        if payload not in ("open", "close"):
            self.publish_alert("WARNING", f"Unknown button payload: {payload}")
            return

        if payload == "open":
            # Rule: do not open if parking is occupied
            if self.parking_occupied:
                self.publish_alert("ALARM", "Open denied: parking is OCCUPIED")
                return
            self.send_gate_command("open")
            self.publish_alert("INFO", "Open command sent")
        else:
            self.send_gate_command("close")
            self.publish_alert("INFO", "Close command sent")

    def handle_gate_ack(self, payload: str):
        # payload: "opened" / "closed"
        if payload == "opened":
            self.gate_open = True
            self.publish_status()
        elif payload == "closed":
            self.gate_open = False
            self.publish_status()
        else:
            self.publish_alert("WARNING", f"Unknown gate ack payload: {payload}")

    # ---------- MQTT callbacks ----------
    def on_connect(self, client, userdata, flags, rc):
        print("Connected to MQTT broker with result code:", rc)
        client.subscribe(TOPIC_SENSOR)
        client.subscribe(TOPIC_BUTTON)
        client.subscribe(TOPIC_GATE_ACK)
        self.publish_status()

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode("utf-8").strip()
        topic = msg.topic

        if topic == TOPIC_SENSOR:
            self.log_event("sensor", topic, payload)
            self.handle_sensor(payload)
        elif topic == TOPIC_BUTTON:
            self.log_event("button", topic, payload)
            self.handle_button(payload)
        elif topic == TOPIC_GATE_ACK:
            self.log_event("gate", topic, payload)
            self.handle_gate_ack(payload)

    def run(self):
        if not DB_PATH.exists():
            print("DB not found. Run: python db/setup_db.py")
        self.client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
        self.client.loop_forever()


if __name__ == "__main__":
    ParkingManager().run()
