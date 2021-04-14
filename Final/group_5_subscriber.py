import json
import time, sys
import random
from datetime import datetime
from typing import Dict
import paho.mqtt.client as mqtt
import group_5_data_generator as dg


class subscriber:
    def __init__()







    def decode_msg(msg):
    msg = msg.decode('utf-8')
    payload = json.loads(msg)
    print("\n----------- Decoded msg -----------\n")
    #(payload)

    def on_connect(mqttc, userdata, flags, rc):
    print('connected...rc=' + str(rc))
    mqttc.subscribe(topic='Final/#', qos=0)


    def on_disconnect(mqttc, userdata, rc):
    print('disconnected...rc=' + str(rc)


    # Create Mqtt client
    mqttc = mqtt.Client()
    # Register callbacks
    mqttc.on_connect = on_connect
    mqttc.on_disconnect = on_disconnect
    mqttc.on_message = on_message
    mqttc.on_subscribe = on_subscribe
    mqttc.on_unsubscribe = on_unsubscribe
    # Connect to Mqtt broker on specified host and port
    mqttc.connect(host='localhost', port=1883)
    # Run Client forever
    mqttc.loop_forever()