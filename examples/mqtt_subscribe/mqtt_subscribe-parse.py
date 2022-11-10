import paho.mqtt.client as mqtt
import config
import json

def on_connect(client, userdata, flags, rc):
    """Callback for when mqtt client connects."""
    print("Connected with result code: " + str(rc))
    # For now, subscribe to the firehose
    client.subscribe("/KV6006/Sensors/#")

def on_message(client, userdata, msg):
    """Callback for when mqtt client receives a message."""
    topic = msg.topic
    # Decode the payload: convert it from bytes to a string...
    payload = msg.payload.decode("utf-8")
    # ...and then parse the string as JSON.
    data = json.loads(payload)
    # print(data)

    for sensor in data['sensors']:
        print("Sensor Name: " + sensor['name'])
        # sensor value is a float, so we need to convert it to a string
        # Note that error messages are suppressed inside MQTT callbacks,
        # so it's very easy to mess this up!
        print("Value: " + str(sensor['value']))

        # If the sensor is a temperature sensor, print the temperature
        # in Fahrenheit as well.
        if sensor['name'] == 'temperature':
            print("Temperature in Fahrenheit: " + str(sensor['value'] * 9 / 5 + 32))



def on_log(mqttc, obj, level, string):
    print(string)

# Now we have our callback functions for connection and message receipt,
# we can go ahead and make a connection.
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_log = on_log
client.username_pw_set(config.mqtt_username, config.mqtt_password)

try:
    client.connect("connect.nustem.uk", 1883, 60)
    print("MQTT connection successful.")
    client.loop_forever()
except:
    print("MQTT connection failed.")
    exit(1)
