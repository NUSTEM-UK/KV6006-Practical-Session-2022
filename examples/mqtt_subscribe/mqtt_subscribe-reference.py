import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    """Callback for when mqtt client connects."""
    # print("Connected with result code "+str(rc))
    # Just get the firehose
    client.subscribe("#") # TODO: QoS setting


def on_message(client, userdata, msg):
    """Callback for when mqtt client receives a message.

    Handles:
    - Connect/NUSTEM/MOOD
    - /management/from/<MAC>
    - /management/to/<MAC>
    - /Connect/NUSTEM/hello_my_name_is
    """
    payload = str(msg.payload.decode("utf-8"))
    # print(msg.topic+" "+payload)

    if (msg.topic == "Connect/NUSTEM/MOOD"):
        # Act on mood
        # TODO: Should we not just log this to a file, and rotate the logs?
        #       Timestamped granularity vs. manual database snapshots.
        #       Yes, but likely also do this, for JSON/AJAX purposes.
        # print("Mood received: ", payload)
        query_string = """
        INSERT INTO moods (mood_name, mood_count)
        VALUES ('"""+payload+"""', 1)
        ON DUPLICATE KEY UPDATE mood_count = mood_count + 1;"""
        db_query(query_string)
        query_string = """
        UPDATE params
            SET paramValue = '"""+payload+"""'
            WHERE paramName = 'current_mood';"""
        db_query(query_string)
    elif (msg.topic.startswith("/management/from")):
        if (payload == "255"):
            # Trigger the device watching function with the MAC address
            # i_see_you(msg.topic[17:29])
            now=datetime.now()
            mac = EUI(msg.topic[17:29])
            query_string = """
            INSERT INTO devices (mac_address, mac_string, last_seen, pings)
            VALUES ('"""+str(int(mac))+"""', '""" + str(mac) + """', '"""+now.strftime("%Y-%m-%d %H:%M:%S")+"""', 1)
            ON DUPLICATE KEY UPDATE
            last_seen = '"""+now.strftime("%Y-%m-%d %H:%M:%S")+"""',
            pings = CASE
                        WHEN pings IS NULL THEN 1
                        ELSE pings + 1
                    END;"""
            db_query(query_string)

    elif (msg.topic.startswith("/management/to")):
        device = int(EUI(msg.topic[15:27]))
        query_string = """
        UPDATE devices SET times_flashed = CASE
                                                WHEN times_flashed IS NULL THEN 1
                                                ELSE times_flashed + 1
                                            END
        WHERE mac_address = '"""+str(device)+"""'
        """
        db_query(query_string)
    elif ('msg.topic.startswith("Connect/NUSTEM/hello_my_name_is")'):
        device = int(EUI(payload))
        now = datetime.now()
        # Update logins count
        query_string = """
        INSERT INTO devices (mac_address, mac_string, logins, last_seen)
        VALUES ('"""+str(device)+"""', '""" + str(EUI(payload)) + """', 1, '"""+now.strftime("%Y-%m-%d %H:%M:%S")+"""')
        ON DUPLICATE KEY UPDATE
        logins = CASE
                    WHEN logins IS NULL THEN 1
                    ELSE logins + 1
                 END,
        last_seen = '"""+now.strftime("%Y-%m-%d %H:%M:%S")+"""'
        ;"""
        db_query(query_string)
        # TODO: handle days active here (separate query?) Or do we do this via MQTT logs?
    else:
        print("Unknown message: ", msg.topic, payload)



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(config.mqttUsername, config.mqttPassword)


if __name__ == "__main__":
    do_connect()
    client.loop_forever()
