import paho.mqtt.client as mqtt
import config

def on_connect(client, userdata, flags, rc):
    """Callback for when mqtt client connects."""
    print("Connected with result code: " + str(rc))
    # For now, subscribe to the firehose
    client.subscribe("/KV6006/Sensors/#")

def on_message(client, userdata, msg):
    """Callback for when mqtt client receives a message."""
    topic = msg.topic
    print(msg.topic)

    try:
        data = json.loads(msg.payload)
    except Exception as e:
        print("Couldn't parse raw data: %s" % msg.paylod, e)
    print("Made it to here")
    print(data)

    payload = msg.payload.decode('utf-8')
    print(payload)
    data = json.loads(msg.payload)

    print(data)
    print(msg.payload.decode("utf-8").rstrip().json())
    payload = msg.payload.decode("utf-8")
    # For now, output the message
    print("Received: " + topic + " " + payload)
    # ...but we'll show how to match a specific topic.
    # It would usually be better to subscribe to only the desired topic

    # data = msg.payload.decode("utf-8").json()
    # for sensor in data['sensors']:
    #     print("Sensor Name: " + sensor['name'])
    #     print("Value: " + sensor["value"])

    # if (topic.startswith("/KV6006/Sensors/ding")):
    #     print("DING!")

# Now we have our callback functions for connection and message receipt,
# we can go ahead and make a connection.
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(config.mqtt_username, config.mqtt_password)

try:
    client.connect("connect.nustem.uk", 1883, 60)
    print("MQTT connection successful.")
    client.loop_forever()
except:
    print("MQTT connection failed.")
    exit(1)
