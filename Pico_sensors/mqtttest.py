import netman
import time
from secrets import ssid, password, mqtt_broker, mqtt_user, mqtt_pass
from umqttsimple import MQTTClient
from machine import Pin

country = 'GB'
wifi_connection = netman.connectWiFi(ssid,password,country)

#mqtt config
client_id = 'PicoW'
topic_pub = 'Connect/NUSTEM/MOOD'

last_message = 0
message_interval = 5
counter = 0

#MQTT connect
def mqtt_connect():
    client = MQTTClient(client_id, mqtt_broker, user=mqtt_user, password=mqtt_pass, keepalive=60)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_broker))
    return client

#reconnect & reset
def reconnect():
    print('Failed to connected to MQTT Broker. Reconnecting...')
    time.sleep(5)
    # machine.reset()


# would normally put this in a while true loop
try:
    client = mqtt_connect()
except OSError as e:
    reconnect()

client.publish(topic_pub, 'SKULL')
print('published')
time.sleep(2)
client.disconnect()
