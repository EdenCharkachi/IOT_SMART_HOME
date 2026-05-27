# IOT Smart Home - Smart Parking Project (MQTT + Python)

This project matches the course requirements:
- **3 emulators**:
  1) Parking sensor emulator (occupied/free)
  2) Gate button emulator (open/close)
  3) Gate relay emulator (actuator): listens for commands and sends ack
- **Data Manager App** (manager.py): collects from broker, logs to DB, processes rules, sends Warning/Alarm messages
- **GUI App** (gui/dashboard.py): shows data, plus Info/Warning/Alarm status
- **Local DB** (SQLite): stores events, snapshots, alerts

## Requirements
- Python 3.10+
- Mosquitto MQTT broker running locally on 127.0.0.1:1883

## Install
```bash
pip install -r requirements.txt
python db/setup_db.py
```

## Run (recommended: multiple terminals)
1) Start Mosquitto broker:
```bash
mosquitto -v
```

2) Start Data Manager:
```bash
python manager.py
```

3) Start emulators:
```bash
python emulators/gate_relay_emulator.py
python emulators/parking_sensor_emulator.py
python emulators/gate_button_emulator.py   # optional (manual commands)
```

4) Start GUI:
```bash
python gui/dashboard.py
```

## MQTT Topics
- home/parking/sensor (occupied/free)
- home/parking/button (open/close)
- home/parking/gate/cmd (open/close)
- home/parking/gate/ack (opened/closed)
- home/parking/status (JSON retained)
- home/parking/alarm (JSON)
