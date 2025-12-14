import os
import requests
import random
import time

# Configuration
API_KEY = os.getenv("API_KEY")
DEVICE_LABEL = "lab12_test_device"
ACTUATION_VARIABLE = "fan"  # Example: variable controlling a fan
HUMIDITY_THRESHOLD_HIGH = 55.0
HUMIDITY_THRESHOLD_LOW = 45.0
URL = f"https://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}/{ACTUATION_VARIABLE}/values"
HEADERS = {
    "X-Auth-Token": API_KEY,
    "Content-Type": "application/json"
}

# Simulate or fetch humidity value
def get_humidity():
    # Replace this with real fetch from CSF if needed
    return random.uniform(40, 60)

def actuate(value):
    data = {"value": value}
    response = requests.post(URL, headers=HEADERS, json=data)
    if response.status_code in [200, 201]:
        print(f"Actuation sent: {value}")
    else:
        print(f"Failed to actuate: {response.status_code} - {response.text}")

if __name__ == "__main__":
    print("Starting actuation monitoring. Press Ctrl+C to stop.")
    while True:
        humidity = get_humidity()
        print(f"Current humidity: {humidity:.1f}%")
        if humidity > HUMIDITY_THRESHOLD_HIGH:
            actuate(1)  # Example: 1 = turn fan ON
        elif humidity < HUMIDITY_THRESHOLD_LOW:
            actuate(0)  # Example: 0 = turn fan OFF
        else:
            print("Humidity normal, no actuation.")
        time.sleep(10)  # Check every 10 seconds
