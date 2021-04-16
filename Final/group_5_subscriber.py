import json
import time, sys
import random
from datetime import datetime
from typing import Dict
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import paho.mqtt.client as mqtt
import group_5_data_generator as dg
import threading

class Subscriber:
    def __init__(self):
        self.mqttc = mqtt.Client()
        # init mqttc messaging part in multi-thread
        sub_thread = threading.Thread(target=self.receive_data, daemon=True)
        sub_thread.start()

        # init gui
        self.bar = self.Bar(fig, ax)
    
    values = list()
    timestamps = list()

    def decode_msg(self, msg):
        msg = msg.decode('utf-8')
        payload = json.loads(msg)
        print("")
        # print("\n----------- Decoded msg -----------\n")
        # self.print_data(payload)
        self.values.append(payload.get('temperature'))
        self.timestamps.append(payload.get('datetime'))
        # refresh gui
        self.values = self.bar.y_val
        self.timestamps = self.bar.x_val
        # self.bar.refresh_plot()
        self.bar.master.event_generate("<<refresh_plot>>", when="tail")

    def print_data(self, payload):
        print(f"Message ID: {payload.get('id')}\n"\
            f"Received Time: {payload.get('datetime')}\n"\
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
        self.mqttc.loop_forever()

    # static methods for mqtt

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
    
    class Bar(Frame, threading.Thread):
        def __init__(self, fig, ax):
            super().__init__()
            self.fig = fig
            self.ax = ax
            self.canvas = Canvas(self)
            self.initUI()

        y_val = list()
        x_val = list()

        def initUI(self):
            self.master.title('Dynamic Display')
            self.position = 0

            # draw outline
            canvas = Canvas(self)
            
            # pack
            canvas.pack(fill=BOTH, expand=1)
            chart_type = FigureCanvasTkAgg(self.fig, root)
            chart_type.get_tk_widget().pack()

            # get_command
            def get_command():
                self.ax.clear()
                self.fig.canvas.flush_events()
                display_plot()
            
            def display_plot():
                self.ax.clear()
                self.ax.plot(self.y_val, "r-")
                self.ax.set_title("IoT thermometer")
                self.ax.set_ylabel("temperature (\N{DEGREE SIGN}C)")
                self.ax.set_yticks([i * 10 for i in range(-3, 6)])
                self.ax.set_yticklabels([i * 10 for i in range(-3, 6)])
                self.fig.canvas.draw()
            
            def eventhandler(evt):
                get_command()

            self.master.bind("<<refresh_plot>>", eventhandler)

# run the code
fig = plt.Figure(figsize=(6,5), dpi=100)
ax = fig.add_subplot(111)
root = Tk()
root.configure(background='white')
root.geometry('600x500')

sub = Subscriber()

root.mainloop()