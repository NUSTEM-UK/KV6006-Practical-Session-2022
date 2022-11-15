import netman
import time
from secrets import ssid, password, mqtt_broker, mqtt_user, mqtt_pass
from umqttsimple import MQTTClient
# from repeated_timer import RepeatedTimer
import machine
import json

country = 'GB'
wifi_connection = netman.connectWiFi(ssid, password, country)

# mqtt config
client_id = "PicoW"
topic_pub = "/KV6006/Sensors"

last_message = 0
message_interval = 5
counter = 0


def mqtt_connect():
    client = MQTTClient(client_id, mqtt_broker, user=mqtt_user,
                        password=mqtt_pass, keepalive=60)
    client.connect()
    print('Connected to %s MQTT Broker' % (mqtt_broker))
    return client


def reconnect():
    print('Failed to connected to MQTT Broker. Reconnecting...')
    time.sleep(5)


try:
    client = mqtt_connect()
except OSError as e:
    reconnect()


temp_sensor = machine.ADC(4)
conversion_factor = 3.3/65535

magnet_sensor = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)
dial_sensor = machine.ADC(0)
force_sensor = machine.ADC(1)

button_blue = machine.Pin(10, machine.Pin.IN, machine.Pin.PULL_UP)
button_yellow = machine.Pin(11, machine.Pin.IN, machine.Pin.PULL_UP)
button_pink = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)
button_green = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)

while True:
    # Slightly dodgy conversion of reading to temperature in Celsius
    # TODO: look into whether this is even vaguely accurate.
    temp_reading = temp_sensor.read_u16() * conversion_factor
    temperature = 27 - (temp_reading - 0.706)/0.001721

    magnet_reading = magnet_sensor.value()
    dial_reading = dial_sensor.read_u16()
    force_reading = force_sensor.read_u16()

    # Construct dictionary
    sensor_data = {"sensors": [
        {"name": "temperature", "value": temperature},
        {"name": "magnet", "value": magnet_reading},
        {"name": "dial", "value": dial_reading},
        {"name": "force", "value": force_reading},
        {"name": "blue", "value": button_blue.value()},
        {"name": "yellow", "value": button_yellow.value()},
        {"name": "pink", "value": button_pink.value()},
        {"name": "green", "value": button_green.value()}
    ]}
    # print(sensor_data)

    # Send JSON data over MQTT
    client.publish(topic_pub, json.dumps(sensor_data))
    print("Published: " + str(sensor_data))
    # print(json.dumps(sensor_data))

    time.sleep(1)
