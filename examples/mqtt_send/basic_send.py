# examples/mqtt_send/basic_send.py
import json
import paho.mqtt.client as mqtt
import config

client = mqtt.Client()

payload = {"name:" "Bob",
           "favourite_colour": "blue",
           "data_value": 328}

mqtt.connect(config.mqtt_server, config.mqtt_port, 60)
mqtt.publish("/KV6006/test", json.dumps(payload))
