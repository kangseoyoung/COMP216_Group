# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 23:19:04 2021

@author: Group 5
"""
from tkinter import *
from group_5_data_generator import temperature_day_records

class Bar(Frame):

    def __init__(self):
        super().__init__()
        self.initUI()
         
    def initUI(self, temperature = 0):
        
        self.master.title('Thermometer')
        self.pack(fill=BOTH, expand=1)
        
        # draw outline
        canvas = Canvas(self)
        canvas.create_rectangle(285, 20, 315, 980,outline='#222')
        
        # draw mark
        temperatureList = ['50°C','40°C','30°C','20°C','10°C','0°C','10°C','20°C','30°C']
        y = 100
        for i in range(9):
            canvas.create_line(320, y + 100 * i, 345, y + 100 * i,width=3)
            canvas.create_text(350, 100 + 100 * i, anchor=W, font='Purisa', text=temperatureList[i])
        for i in range(40):
            canvas.create_line(320, y + 20 * i, 335, y + 20 * i)
            
        # draw mercury
        y = 600 - abs(temperature)/80 * 800
        self.mercury = canvas.create_rectangle(
            290, y,                  #top left
            310, 975,                  #bottom right
        outline='#222', fill='red')
        
        # input temperature
        canvas.create_text(10, 100, anchor=W, font='Purisa', text='Input current temperature')
        e1 = Entry(canvas)
        canvas.create_window(130,120,window=e1)
        
        # refresh temperature
        button1 = Button(self, text = "Refresh", command = lambda: canvas.coords(self.mercury, 290, 600 - abs(int(e1.get()))/80 * 800, 310, 975), anchor = W)
        button1_window = canvas.create_window(100, 135, anchor=NW, window=button1)
        
        # pack
        canvas.pack(fill=BOTH, expand=1)
        
    '''
    def refreshTemperature(self, temperature = 0):  
        print('refreshTemperature')
        print(temperature)
        temperature = int(temperature)
        y = 600 - abs(temperature)/80 * 800
        canvas = Canvas(self)
        canvas.coords(self.mercury, 290, y, 310, 975)
    '''
        
root = Tk()
bar = Bar()
root.geometry('600x1000')
root.mainloop()
