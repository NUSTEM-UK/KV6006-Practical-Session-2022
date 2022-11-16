# examples/mqtt_send/control_device.py
import paho.mqtt.client as mqtt
import config
import json
from time import sleep

def on_publish(client, userdata, result):
    print("Data published")
    pass

# TODO: Change the client name here to reflect your device code
client = mqtt.Client("controlD31")
client.on_publish = on_publish
client.username_pw_set(config.mqtt_username, config.mqtt_password)

try:
    client.connect("connect.nustem.uk", 1883, 60)
    print("MQTT connection successful")
except:
    print("MQTT connection failed")
    exit(1)

# TODO: Again, change the target device here
target = "/KV6006/output/D31"
# Set up a dictionary structure for command and value to pass
message = {"command": "LEDhue",
            "value": 60}
# Send message, converting payload to JSON
client.publish(target, json.dumps(message))

message = {"command": "servoAngle",
            "value": 180}
client.publish(target, json.dumps(message))

# 2-second pause
sleep(2)

message = {"command": "servoAngle",
            "value": 0}
client.publish(target, json.dumps(message))
