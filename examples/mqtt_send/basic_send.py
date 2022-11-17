# examples/mqtt_send/basic_send.py
import json
import paho.mqtt.client as mqtt
import config

# TODO: Change the client name here, it has to be unique.
client = mqtt.Client("Control_D55")
client.username_pw_set(config.mqtt_username, config.mqtt_password)
client.connect(config.mqtt_server, config.mqtt_port, 60)

# TODO: Change the target device here. It's written on a label stuck to the control board
topic = "/KV6006/output/D55"

payload = {"command": "LEDhue", "value": 120}
client.publish(topic, json.dumps(payload))

payload = {"command": "servoAngle", "value": 30}
client.publish(topic, json.dumps(payload))
