# KV6006 practical session - 3 - MQTT

Arguably, the core of Internet of Things systems is the message-passing protocol MQTT. The letters used to stand for something like 'Message Queue Telemetry Transport' but there was never really a 'queue'. Officially it's no longer even pretending to be an acronym.

## Topics and Payloads

An MQTT message originates from a data source, which publishes it to a 'broker' – server – which in turn retransmits the message to anything that's subscribed to listen to it. Messages are sent on specific 'topics', which are named like:

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

You'll notice a steady stream of data on the `/KV6006/Sensors` topic. This is coming from a device at the front of the room: a Raspberry Pi Pico W microcontroller connected to a bunch of different sensors. A MicroPython script on the Pico polls data from the sensors, packages it as JSON, and broadcasts it over MQTT. It's connected to a WiFi network from a 4G mobile router. The MQTT broker is physically in London, by the way.

The sensors data feed is formatted as JSON. So you can expand your `on_message()` function to do something like:

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

The sensor `value` is of type `float`, and we have to explicitly convert it to a string with `str()`.

> NOTE: the Paho MQTT package we're using suppresses error messages in the `on_message()` callback. Which makes debugging infuriatingly difficult. You can work around this by adding `client.on_log = on_long` to the configuration after the `client.on_connect` and `client.on_message` lines. However, you'll see a *lot* of diagnostics.

### Getting just some of the data

Suppose you wanted just the temperature sensor data. Unfortunately, there isn't a useful key you can access: something like `data['sensors']['temperature']` won't work. It's possible my Python-fu just isn't strong enough, but I think you'd have to do something like:


```python
for sensor in data ['sensors']:
    if sensor['name'] == 'temperature':
        print("Temperature is: " + str(sensor['value']))
```

This probably illustrates that I should have thought more carefully about the JSON structure of the sensor data, or broken the individual sensors out into different MQTT topics.

Think about (and discuss) how the sensor data could be better structured.

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

You could wrap the last two lines in a `try / except` structure, but for our purposes today it's not terribly important. The `json.dump()` method handles converting the Python dictionary `payload` into JSON format for us.

## Controlling a device over MQTT

Finally, we get to the odd little device which has been sitting next to your Raspberry Pi all along. This is an even simpler microcontroller than the Pico - the little blue thing is an ESP8266, which is about as cheap as WiFi-enabled boards get. It's sitting on a chunk of breadboard (the white slab with holes in it), wired up to two output devices:

- An RGB LED, which can display a range of colours at variable brightness.
- A servo motor, which can turn its 'horn' through about 180 degrees.

The code these boards are running was originally written five or so years ago, for an installation art project. The code is... mmm, *not good*. However, it still works. Mostly.

Each device listens for commands via its own MQTT topic, `/KV6006/output/[device_code]`. The device code is printed on a sticker on the ESP8266.

You can command the device using something like:

```python
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
```

You can probably work out what this is intended to do.

### A note about colour

Colour representation is one of *those* subjects. You'd think it would be easy, but... no. Not as such.

Most computer systems *display* full colour by mixing red, green and blue (RGB) light emitters (LEDs, or phosphor dots on an old-fashioned tube monitor and wow do I feel old typing that). These three colours correspond fairly well to the receptors in our eyes, and you can cover a pretty decent range of colours by mixing them together.

Typically, each colour scales in brightness from `0` (off) to `255` (full brightness). 255 is chosen because it's the largest integer you can represent in 8 bits, which means each pixel takes 24 bits of data. In theory the human eye can't distinguish that many brightness steps, though in practice it turns out 24-bit colour isn't *quite* good enough in all circumstances.

Whatever, the output device has precisely one pixel. It has separate red, green and blue emitters, and the internal data model is 8 brightness bits per emitter.

BUT: it's really hard to work out what colour you're going to get when you start mixing red, green and blue. In many circumstances, it's more convenient to just pick a colour and ask for that. Welcome to HSV colour space.

Rather than RGB – which feels like it *ought* to make sense, but doesn't - HSV seems horrendous, but is somehow easier. It's still 3x8-bits, with the channels being:

* **Hue**. An arbitrary figure, typically representing an angle around a wheel of colours.
* **Saturation**. How intense is the hue, within the brightness range?
* **Value**. Which is more-or-less overall brightness, sometimes described as Lightness ('HSL space') or brightness ('HSB space').

You may have spotted a problem here: circles traditionally cover 360 degrees, which is a bigger number than 255. So, yes, we represent Hue *angle* on a scale from 0..255. Just roll with it. The scale looks like this:

![Hue angle image](images/HueScale.png)

TL;DR: guess a Hue value from the chart above, pass that to the output device, and it'll show... mmm, something vaguely related. Colour *matching* is a whole other problem.

## Things to do at this point

- `LEDhue` and `servoAngle` aren't great names for commands. More common would be `setLEDhue` and `setServoAngle`. Why?
- If you're _really_ keen, the code the ESP8266s are running is in this repository, in the `output_devices` directory. For obscure reasons these things got called 'Skutters'. By all means take a look at the code, and see if you can work out some of the API calls I've not mentioned. Hint: The original devices stored two states, 'A' and 'B', and animated changes between them.
- If you find the command to change the LED brightness, be warned that full brightness is eye-searingly horrid. Don't say I didn't warn you.
