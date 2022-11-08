# KV6003 practical session - 3 - MQTT

Arguably, the core of Internet of Things systems is the message-passing protocol MQTT. The letters used to stand for something like 'Messasge Queue Telemetry Transport' but there was never really a 'queue'. Officially it's no longer even pretending to be an acronym.

## Topics and Payloads

An MQTT message originates from a data source, which publishes it to a 'broker' - server - which retransmits the message to anything that's subscribed to listen to it. Messages are sent on specific 'topics', which are named like:

> `/Northumbria/City_Campus/Ellison_Building/E_Block/305`

The topic doesn't need to already exist before a client publishes or subscribes to it. Subscribers can specify wildcards:

> `/Northumbria/City_Campus/+/E_Block/+`

The `+` is a single-level wildcard, so this would match any building on City Campus that has an 'E_Block', then any room in that building.

> `/Northumbria/City_Campus/#`

`#` matches any number of levels, so this would match _everything_ on City Campus. On a busy MQTT broker, `/#` might involve quite a lot of messages.

## Subscribing to MQTT messages

We're going to use the Paho MQTT client library in Python, and we've a little bit of setup to do. In a fresh Thonny document:

```python
import paho.mqtt.client as mqtt
import config

def on_connect(client, userdata, flags, rc):
    """Callback for when mqtt client connects."""
    print("Connected with result code: " + str(rc))
    # For now, subscribe to the firehose
    client.subscribe("/kv6003/#")

def on_message(client, userdata, msg):
    """Callback for when mqtt client receives a message."""
    topic = msg.topic
    payload = str(msg.payload.decode("utf-8"))
    # For now, output the message
    print(topic + " " + payload)
    # ...but we'll show how to match a specific topic.
    # It would usually be better to subscribe to only the desired topic
    if (topic.startswith("/kv6003/sensor/ding")):
        print("DING!")

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
```

If all goes well, the `client.loop_forever()` line will keep the program running. When a message is received, `on_message()` is called to handle it - you should see messages being output.

If the connection drops the program will likely crash; in a real-world situation you'd want to be a bit more robust in your error handling. That said, I've had very similar code to the above running on a server for almost a year without issue.

## Sending MQTT messages

This is even simpler:

```python
import json
import paho.mqtt.client as mqtt
import config

client = mqtt.Client()

payload = {"name:" "Bob",
           "favourite_colour": "blue",
           "data_value": 328}

mqtt.connect(config.mqtt_server, config.mqtt_port, 60)
mqtt.publish("KV6003/test", json.dumps(payload))
```

You _could_ wrap the last two lines in a `try / except` block, but for our purposes today it's not terribly important.
