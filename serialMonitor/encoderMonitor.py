from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
import serial
import os
import time


class Window(tk.Tk):
    def __init__(self, virtual = False):
        super().__init__()
        self.title("encoder monitor")
        self.geometry("1280x800")

        self.virtual = virtual

        self.init_widgets()
        self.init_values()
        self.init_serial()
        self.init_graph()
        self.init_ani()

        self.mainloop()

    def init_widgets(self):
        self.grid_rowconfigure(0, weight=1)

        self.viewframe = tk.Frame(self)
        self.viewframe.grid(row=0, column=0)
        self.viewframe.grid_rowconfigure(0, weight=1)
        self.viewframe.grid_columnconfigure(0, weight=1)
        self.fig, self.ax = plt.subplots(2, 1)
        self.canvas = FigureCanvasTkAgg(self.fig, self.viewframe)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0,column=0)

        self.entryframe = tk.Frame(self)
        self.entryframe.grid(row=1, column=0)
        self.entries = [tk.Entry(self.entryframe) for i in range(6)]
        for i, entry in enumerate(self.entries):
            entry.grid(row=0, column=i)
        self.button = tk.Button(self.entryframe, text="Run", command=self.run)
        self.button.grid(row=0, column=6)

    def init_values(self):
        for i, v in enumerate(['1.3', '0.06', '0', '0.00004', '0.000001', '0']):
            self.entries[i].insert(0, str(v))

    def init_serial(self):
        self.serial = serial.Serial()
        self.serialbaudrate = 9600
        for file in os.listdir('/dev'):
            if "tty.usbmodem" in file:
                self.serial.port = '/dev/'+file
                self.serial.open()
                break
        else:
            self.virtual = True
        
    def init_graph(self):
        self.T = time.time()
        self.t = list(np.arange(-20,0,0.1))
        self.speedTargetList = np.zeros(200).tolist()
        self.speedList = np.zeros(200).tolist()
        self.amountTargetList = np.zeros(200).tolist()
        self.amountList = np.zeros(200).tolist()
    
    def init_ani(self):
        self.update()

    def run(self):
        try:
            [float(entry.get()) for entry in self.entries]
        except:
            print([entry.get() for entry in self.entries])
            return
        
        if not self.virtual:
            self.serial.write((",".join([entry.get() for entry in self.entries])+'\n').encode())
            

    def update(self):
        line = None
        if not self.virtual:
            line = self.serial.readline().decode().replace('\n','').replace('\r','')
            print(line)
            try:
                if len([int(v) for v in line.split(",")]) != 4:
                    self.after(1, self.update)
                    return
            except:
                #print(line)
                self.after(1, self.update)
                return

            if line is not None:
                speedTarget, speed, amountTarget, amount = [int(v) for v in line.split(",")]
            else:
                self.after(1, self.update)
                return
        else:
            speedTarget, speed, amountTarget, amount = np.random.randn(4)

        self.t.pop(0)
        self.t.append(time.time() - self.T)

        self.speedTargetList.pop(0)
        self.speedTargetList.append(speedTarget)

        self.speedList.pop(0)
        self.speedList.append(speed)
        
        self.amountTargetList.pop(0)
        self.amountTargetList.append(amountTarget)

        self.amountList.pop(0)
        self.amountList.append(amount)

        self.ax[0].set_xlim((self.t[0], self.t[-1]))
        self.ax[1].set_xlim((self.t[0], self.t[-1]))

        self.ax[0].plot(self.t, self.speedTargetList, color='C1', linestyle='--')
        self.ax[0].plot(self.t, self.speedList, color='C0', linestyle='-')
        self.ax[1].plot(self.t, self.amountTargetList, color='C1', linestyle='--')
        self.ax[1].plot(self.t, self.amountList, color='C0', linestyle='-')

        self.canvas.draw()

        self.after(1, self.update)


    

Window()


    
            



