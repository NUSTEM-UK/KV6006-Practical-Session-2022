import paho.mqtt.client as mqtt
import config
import json
from time import sleep

def on_publish(client, userdata, result):
    print("Data published: ")

    pass

client = mqtt.Client("control")
client.on_publish = on_publish
client.username_pw_set(config.mqtt_username, config.mqtt_password)

try:
    client.connect("connect.nustem.uk", 1883, 60)
    print("MQTT connection successful")
except:
    print("MQTT connection failed")
    exit(1)

# FIXME: Change the target device here!
target = "/KV6006/output/D32"

# message = {"command": "setLEDhue",
#             "position": "",
#             "state": "B",
#             "value": 120}
# message_json = json.dumps(message)
# client.publish(target, message_json)

message = {"command": "LEDhue",
            "value": 128}
message_json = json.dumps(message)
client.publish(target, message_json)

message = {"command": "servoAngle",
            "value": 0}
message_json = json.dumps(message)
client.publish(target, message_json)

sleep(1)

message = {"command": "servoAngle",
            "value": 180}
message_json = json.dumps(message)
client.publish(target, message_json)

# message = {"command": "setServoPosition",
#             "servoNum": 1,
#             "state": "B",
#             "angle": 180}
# message_json = json.dumps(message)
# client.publish(target, message_json)

sleep(1)

message = {"command": "LEDhue",
            "value": 42}
message_json = json.dumps(message)
client.publish(target, message_json)
