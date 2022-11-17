# examples/mqtt_send/control_device.py
import paho.mqtt.client as mqtt
import config
import json
from time import sleep


def on_publish(client, userdata, result):
    print("Data published")
    pass


def on_connect(client, userdata, flags, rc):
    """Callback for when mqtt client connects."""
    print("Connected with result code: " + str(rc))
    # Retrieve sensor data
    client.subscribe("/KV6006/Sensors/#")
    print("Subscribed to sensors")


def rescale(x, in_min, in_max, out_min, out_max):
    """Rescale a value from one range to another."""
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def on_message(client, userdata, msg):
    """Callback for when mqtt client receives a message."""
    topic = msg.topic
    # Decode the payload: convert it from bytes to a string...
    payload = msg.payload.decode("utf-8")
    # ...and then parse the string as JSON.
    data = json.loads(payload)

    # Set up any temporary variables here, eg:
    hue_to_send = 0

    for sensor in data["sensors"]:
        # Match against individual sensors here. Example included.

        # If the sensor is the blue button, check if it's pressed (value 0)
        # and if so, set the hue angle accordingly.
        if sensor["name"] == "blue" and sensor["value"] == 0:
            print("Blue!")
            hue_to_send = 170

        # You might publish a message here.
        # Alternatively, do it outside the sensor parsing loop:

    # We've now been through all the sensors, so act on what we've learned:

    # Check to see if we have a hue angle set
    if hue_to_send != 0:
        # Set up a dictionary structure for command and value to pass
        payload = {"command": "LEDhue", "value": hue_to_send}
        # Send message, converting payload to JSON
        client.publish(target, json.dumps(payload))


# TODO: Replace the output device here
target = "/KV6006/output/D55"

# TODO: Change the client name here to reflect your device code
client = mqtt.Client("controlD55")
client.on_publish = on_publish
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(config.mqtt_username, config.mqtt_password)

# Uncomment to enable debug messages
# client.on_log = on_log

try:
    client.connect("connect.nustem.uk", 1883, 60)
    print("MQTT connection successful.")
    client.loop_forever()
except:
    print("MQTT connection failed.")
    exit(1)
