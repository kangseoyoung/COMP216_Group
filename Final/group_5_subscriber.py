import json
import time, sys
import random
from datetime import datetime
from typing import Dict
import paho.mqtt.client as mqtt
import group_5_data_generator as dg
import threading

class subscriber:
    def __init__(self):
        self.mqttc = mqtt.Client()
        # init mqttc messaging part in multi-thread
        self.msg_thread = threading.Thread(target=self.receive_data, daemon=True)
        self.msg_thread.start()

    def decode_msg(self, msg):
        msg = msg.decode('utf-8')
        payload = json.loads(msg)
        print("\n----------- Decoded msg -----------\n")
        self.print_data(payload)

    def print_data(self, payload):
        print(f"Message ID: {payload.get('id')}\n"\
            f"Received Time: {payload.get('time')}\n"\
            f"Temperature: {payload.get('temperature')}\n"\
            f"Unit: {payload.get('unit')}\n"\
            f"Serial Number: {payload.get('serial')}\n")

    def receive_data(self) -> None:
        self.mqttc.on_connect = self._on_connect
        self.mqttc.on_disconnect = self._on_disconnect
        self.mqttc.on_message = self._on_message
        self.mqttc.on_subscribe = self._on_subscribe
        self.mqttc.on_unsubscribe = self._on_unsubscribe
        self.mqttc.connect(host='broker.emqx.io', port=1883)

    def _on_connect(self, mqttc, userdata, flags, rc):
        print('connected...rc=' + str(rc))
        mqttc.subscribe(topic='iot/measure/thermometer', qos=0)


    def _on_disconnect(self, mqttc, userdata, rc):
        print('disconnected...rc=' + str(rc))

    def _on_message(self, mqttc, userdata, msg):
        print("Received message --------")
        print('topic: ' + msg.topic + ', qos: ' + 
            str(msg.qos) + ', message: ' + str(msg.payload))
        self.decode_msg(msg.payload)
    
    def _on_subscribe(self, mqttc, userdata, mid, granted_qos):
        print('subscribed (qos=' + str(granted_qos) + ')')

    def _on_unsubscribe(self, mqttc, userdata, mid, granted_qos):
        print('unsubscribed (qos=' + str(granted_qos) + ')')

sub1 = subscriber()
sub1.mqttc.loop_forever()