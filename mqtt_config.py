# MQTT configuration + topics
BROKER_HOST = "127.0.0.1"
BROKER_PORT = 1883

# Producers (emulators)
TOPIC_SENSOR = "home/parking/sensor"          # payload: "occupied" / "free"
TOPIC_BUTTON = "home/parking/button"          # payload: "open" / "close"

# Actuator command + feedback (gate relay emulator)
TOPIC_GATE_CMD = "home/parking/gate/cmd"      # payload: "open" / "close"
TOPIC_GATE_ACK = "home/parking/gate/ack"      # payload: "opened" / "closed"

# System outputs
TOPIC_STATUS  = "home/parking/status"         # JSON status (retained)
TOPIC_ALARM   = "home/parking/alarm"          # JSON warning/alarm messages
