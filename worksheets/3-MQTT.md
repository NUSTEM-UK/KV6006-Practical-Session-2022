# KV6006 practical session - 3 - MQTT

Arguably, the core of Internet of Things systems is the message-passing protocol MQTT. The letters used to stand for something like 'Messasge Queue Telemetry Transport' but there was never really a 'queue'. Officially it's no longer even pretending to be an acronym.

## Topics and Payloads

An MQTT message originates from a data source, which publishes it to a 'broker' – server – which retransmits the message to anything that's subscribed to listen to it. Messages are sent on specific 'topics', which are named like:

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
import json

def on_connect(client, userdata, flags, rc):
    """Callback for when mqtt client connects."""
    print("Connected with result code: " + str(rc))
    # For now, subscribe to the firehose
    client.subscribe("/KV6006/#")

def on_message(client, userdata, msg):
    """Callback for when mqtt client receives a message."""
    topic = msg.topic
    # Decode the payload: convert it from bytes to a string
    payload = str(msg.payload.decode("utf-8"))
    # For now, output the message
    print(topic + " " + payload)

def on_log(mqttc, obj, level, string):
    print(string)

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

## Parsing data received over MQTT

You'll notice that the data you're receiving on the `KV6006/Sensors` topic is formatted as JSON. So you can expand your `on_message()` function to do something like:

```python
# [...]
payload = msg.payload.decode("utf-8")
# Parse  the string as JSON
data = json.loads(payload)

# Now we can iterate over the sensor data:
for sensor in data['sensors']:
    print("Sensor: " + sensor['name'])
    print("Value: " + str(sensor['value']))
```

The sensor value is of type float, and we have to explicitly convert it to a string with `str()`.

> NOTE: the Paho MQTT package we're using suppresses error messages in the `on_message()` callback. Which makes debugging infuriatingly difficult. You can work around this by adding `client.on_log = on_long` to the configuration after `client.on_connect` and `client.on_message` lines. However, you'll see a *lot* of diagnostics.

### Getting just some of the data

Suppose you wanted just the temperature sensor data. Unfortunately, there isn't a useful key you can access: something like `data['sensors']['temperature']` won't work. It's possible my Python-fu just isn't strong enough, but I think you'd have to do something like:


```python
for sensor in data ['sensors']:
    if sensor['name'] == 'temperature':
        print("Temperature is: " + str(sensor['value']))
```

This probably illustrates that I should have thought more carefully about the JSON structure of the sensor data, or broken the individual sensors out into different MQTT topics.

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
mqtt.publish("KV6006/test", json.dumps(payload))
```

You _could_ wrap the last two lines in a `try / except` block, but for our purposes today it's not terribly important. The `json.dump()` method handles converting the Python dictionary `payload` into JSON format for us.

## Putting it together

You'll have noticed that the device on the `KV6006/Sensors` topic is sending JSON-formatted data, containing a list of sensors and their current values. So we can modify the `on_message()` function in our data
