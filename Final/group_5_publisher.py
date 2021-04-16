import json
import time
import sys
import random
import threading
from datetime import datetime
from typing import Dict
from tkinter import *
import paho.mqtt.client as mqtt
import group_5_data_generator as dg

class Publisher:
    def __init__(self, start_id: int = None, max_msg: int = None) -> None:
        self.start_id: int = start_id or 100
        self.max_msg: int = max_msg or 500
        self.sample_set = dg.sample_set()
        # each publisher represents an IoT thermometer
        # each IoT thermometer has an unique serial number
        self.serial = "SN"+ f"{round(random.random(), 12)}"[2:] # generate a virtual serial number
        # init gui
        self.bar = Bar(self.serial)
        # init mqttc messaging part in multi-thread
        self.pub_thread = threading.Thread(target=self.send_data, daemon=True)
        self.pub_thread.start()
    
    temperature: float = 0

    # get a single value from generator
    def get_data(self) -> float:
        return self.sample_set.data

    # packaging the above value
    def create_data(self) -> Dict[str, str]:
        self.start_id += 1
        self.temperature = self.get_data() # get the temperature from the method
        # outlier generator
        virtual_outlier_adds = random.randint(1, 100)
        if (virtual_outlier_adds == 50): # TODO: CHANGE THIS, ODDS IS HIGHER THAN THE STANDARD JUST FOR A TEST
            self.temperature += random.randint(20, 40)
        payload = {
            "id": f"{self.start_id}",
            "datetime": f"{datetime.now()}",
            "temperature": f"{self.temperature:.2f}",
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
            virtual_failure_odds = random.randint(1, 100) # for the virtual failure
            time.sleep(1) # Sleep
            try:
                msg_dict = self.create_data() # get mqss data dict
                data = json.dumps(msg_dict)
                # following the possibility, the message is published or withdraw it
                # since the gui represents the thermometer, it shows the temperature normally
                if (virtual_failure_odds == 50): # TODO: CHANGE THIS, ODDS IS HIGHER THAN THE STANDARD JUST FOR A TEST
                    # withdraw the message
                    print("Published msg: ERROR!")
                else:
                    # publish the message
                    mqttc.publish(topic='iot/measure/thermometer', payload=data, qos=0)
                    print(f"Published msg: {msg_dict}")
            except (KeyboardInterrupt, SystemExit):
                mqttc.disconnect()
                sys.exit()
        
            # refresh GUI
            self.bar.temperature = self.temperature
            self.bar.refresh()

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
    
# GUI
class Bar(Frame):
    def __init__(self, serial: str) -> None:
        super().__init__()
        self.serial: str = serial
        self.canvas = Canvas(self)
        self.entry = Entry(self.canvas)
        self.initUI()
    
    temperature: float = 0
        
    def initUI(self) -> None:
        self.master.title('Thermometer')
        self.pack(fill=BOTH, expand=1)
        
        # draw outline
        self.canvas.create_rectangle(285, 20, 315, 980,outline='#222')
        
        # draw mark
        temperatureList = ['50°C','40°C','30°C','20°C','10°C','0°C','10°C','20°C','30°C']
        y = 100
        for i in range(9):
            self.canvas.create_line(320, y + 100 * i, 345, y + 100 * i,width=3)
            self.canvas.create_text(350, 100 + 100 * i, anchor=W, font='Purisa', text=temperatureList[i])
        for i in range(40):
            self.canvas.create_line(320, y + 20 * i, 335, y + 20 * i)
            
        # draw mercury
        y = 600 - abs(self.temperature)/80 * 800
        self.mercury = self.canvas.create_rectangle(
            290, y,                  #top left
            310, 975,                #bottom right
        outline='#222', fill='red')
        
        # prepare gui
        self.canvas.create_text(20, 75, anchor=W, font='Purisa', text=self.serial)
        self.canvas.create_text(20, 95, anchor=W, font='Purisa', text='Current Temperature:')
        self.canvas.create_window(130,120,window=self.entry)
        
        # pack
        self.canvas.pack(fill=BOTH, expand=1)
        
    # refresh command
    def refresh(self):
        self.entry.delete(0, 'end')
        self.entry.insert(0,f"{self.temperature:.2f}")
        self.canvas.coords(self.mercury, 290, 600 - abs(self.temperature)/80 * 800, 310, 975)

# run the code
root = Tk()
root.geometry('450x1000')
pub = Publisher()
root.mainloop()