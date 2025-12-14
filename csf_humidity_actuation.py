import time
from collections import deque
import paho.mqtt.client as mqtt

# ---------- Configuration ----------
MQTT_BROKER = "127.0.0.1"  # Replace with your cloud broker if needed
MQTT_PORT = 1883            # 8883 for TLS, 1883 for local non-TLS
MQTT_USER = ""              # Add your cloud username if required
MQTT_PASS = ""              # Add your cloud password if required
HUMIDITY_TOPIC = "sensor/humidity"   # Topic where CDA/GDA publishes humidity
ACTUATION_TOPIC = "actuation/humidity_fan"

HUMIDITY_THRESHOLD = 55.0  # %
WINDOW_SIZE = 30            # Number of readings to average

# ---------- Store last N humidity readings ----------
humidity_history = deque(maxlen=WINDOW_SIZE)

# ---------- MQTT Callbacks ----------
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe(HUMIDITY_TOPIC)
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    try:
        humidity = float(msg.payload.decode())
        humidity_history.append(humidity)
        average_humidity = sum(humidity_history) / len(humidity_history)

        print(f"Current humidity: {humidity:.1f}% | Average last {len(humidity_history)} samples: {average_humidity:.1f}%")

        # Actuation logic
        if average_humidity > HUMIDITY_THRESHOLD:
            client.publish(ACTUATION_TOPIC, 1)
            print("Actuation sent: 1 (fan ON)")
        else:
            client.publish(ACTUATION_TOPIC, 0)
            print("Actuation sent: 0 (fan OFF)")

    except ValueError:
        print(f"Received non-numeric humidity value: {msg.payload}")

# ---------- MQTT Client Setup ----------
client = mqtt.Client()
if MQTT_USER and MQTT_PASS:
    client.username_pw_set(MQTT_USER, MQTT_PASS)
# Uncomment the next line for TLS if using cloud broker
# client.tls_set()

client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT)
client.loop_start()

# ---------- Keep script running ----------
try:
    while True:
        time.sleep(1)  # just keep the script alive

except KeyboardInterrupt:
    print("Stopping CSF actuation monitor...")
    client.loop_stop()
    client.disconnect()
