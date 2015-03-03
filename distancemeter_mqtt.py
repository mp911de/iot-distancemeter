__author__ = 'mp911de'

import socket
import json
import time
from distancemeter import get_distance, cleanup
import paho.mqtt.client as mqtt

# MQTT Settings
MQTT_HOST = '192.168.55.34'
MQTT_PORT = 1883

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))



# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


CM_PER_SEC_AIR = 34300

if __name__ == '__main__':
    client = mqtt.Client()

    try:
        client.on_connect = on_connect
        client.connect(MQTT_HOST, MQTT_PORT, 60)

        client.loop_start()

        while True:
            distance = get_distance()
            print ("Received distance = %.1f cm" % distance)
            data = {'message': 'distance %.1f cm' % distance, 'distance': distance, 'hostname': socket.gethostname()}
            client.publish("sensors/distancemeter", json.dumps(data))
            time.sleep(0.2)

    # interrupt
    except KeyboardInterrupt:
        print("Programm interrupted")
        client.loop_stop()
        client.disconnect()
        cleanup()