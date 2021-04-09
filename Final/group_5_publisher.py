import json
import time, sys
import random
from datetime import datetime
from typing import Dict
import paho.mqtt.client as mqtt
import group_5_data_generator as dg

class publisher:
    def __init__(self, start_id: int = None, max_msg: int = None) -> None:
        self.start_id = start_id or 100
        self.max_msg = max_msg or 500
        self.sample_set = dg.sample_set()
        # each publisher represents an IoT thermometer
        # each IoT thermometer has an unique serial number
        # below code generates the unique S/N using time
        self.serial = "SN"+ f"{round(random.random(), 12)}"[2:]

    # get a single value from generator
    def get_data(self) -> float:
        return self.sample_set.data

    # packaging the above value
    def create_data(self) -> Dict[str, str]:
        # hosts = ["google.com", "yahoo.com", "facebook.com", "twitter.com"] # TODO I reckon this is useless
        self.start_id += 1
        payload = {
            "id": f"{self.start_id}",
            "time": f"{datetime.now()}",
            "temperature": f"{self.get_data():.2f}",
            "unit": "celsius",
            "serial": self.serial
        }
        return payload
    
    # send data

    def send_data(self) -> None:
        mqttc = mqtt.Client()
        mqttc.on_connect = self._on_connect
        mqttc.on_disconnect = self._on_disconnect
        mqttc.on_message = self._on_message
        mqttc.on_publish = self._on_publish
        mqttc.connect(host='broker.emqx.io', port=1883)

        for _ in range(self.max_msg):
            try:
                msg_dict = self.create_data() # get mqss data dict
                data = json.dumps(msg_dict)
                mqttc.publish(topic='iot/measure/thermometer', payload=data, qos=0)
                print("Published msg: {}".format(msg_dict))
                time.sleep(5) # Sleep
            except (KeyboardInterrupt, SystemExit):
                mqttc.disconnect()
                sys.exit()

    # static methods for mqtt

    def _on_connect(self, mqttc, userdata, flags, rc):
        print('connected...rc=' + str(rc))

    def _on_disconnect(self, mqttc, userdata, rc):
        print('disconnected...rc=' + str(rc))

    def _on_message(self, mqttc, userdata, msg):
        print('message received...')
        print('topic: ' + msg.topic + ', qos: ' + 
            str(msg.qos) + ', message: ' + str(msg.payload))

    def _on_publish(self, mqttc, userdata, mid):
        print("Message published ID :{}".format(mid))

