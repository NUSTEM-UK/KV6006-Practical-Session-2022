import paho.mqtt.client as mqtt
import config
import json

def on_publish(client, userdata, result):
    print("Data published")
    pass

client = mqtt.Client("control")
client.on_publish = on_publish
client.username_pw_set(config.mqtt_username, config.mqtt_password)

try:
    client.connect("connect.nustem.uk", 1883, 60)
    print("MQTT connection successful")
    target = "/KV6006/output/D31"
    message = {"command": "setLEDhue",
                "position": "",
                "state": "B",
                "value": 240}
    message_json = json.dumps(message)
    client.publish(target, message_json)
except:
    print("MQTT connection failed")
    exit(1)
