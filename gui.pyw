#!/bin/python3

from tkinter import *
from tkinter.ttk import *
from data_thread import *
from filter import filter

import matplotlib
#matplotlib.use('TkAgg')
#import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import datetime

import sys


class value_frame:
    def __init__(self, frame):
        self.frame = frame
        vLab = Label(frame, text='Value:')
        vLab.grid(row=0, column=0, sticky='E', padx=10, pady=10)
        aLab = Label(frame, text='Average:')
        aLab.grid(row=1, column=0, sticky='E', padx=10, pady=10)
        mLab = Label(frame, text='Median:')
        mLab.grid(row=2, column=0, sticky='E', padx=10, pady=10)
        mnLab = Label(frame, text='Min:')
        mnLab.grid(row=3, column=0, sticky='E', padx=10, pady=10)
        mxLab = Label(frame, text='Max:')
        mxLab.grid(row=4, column=0, sticky='E', padx=10, pady=10)
        self.dval = StringVar()
        self.davg = StringVar()
        self.dmed = StringVar()
        self.dmin = StringVar()
        self.dmax = StringVar()
        vEnt = Label(frame, textvariable=self.dval, width=15)
        vEnt.grid(row=0, column=1, sticky='W', padx=10, pady=10)
        aEnt = Label(frame, textvariable=self.davg, width=15)
        aEnt.grid(row=1, column=1, sticky='W', padx=10, pady=10)
        mEnt = Label(frame, textvariable=self.dmed, width=15)
        mEnt.grid(row=2, column=1, sticky='W', padx=10, pady=10)
        mnEnt = Label(frame, textvariable=self.dmin, width=15)
        mnEnt.grid(row=3, column=1, sticky='W', padx=10, pady=10)
        mxEnt = Label(frame, textvariable=self.dmax, width=15)
        mxEnt.grid(row=4, column=1, sticky='W', padx=10, pady=10)


class App(Tk):
    def __init__(self):
        super().__init__()

        self.title('My app')

        self.menu = Menu(self)
        self.menu.add_command(label="Start", command=self.startStop)
        self.menu.add_command(label="Exit", command=self.kill)
        self.config(menu=self.menu)

        self.controlFrm = LabelFrame(self, text='Control')
        self.controlFrm.pack(expand=True, fill='both', padx=10, pady=10)
        self.startBtn = Button(self.controlFrm, text='Start', command=self.startStop)
        self.startBtn.pack(padx=10, pady=10, side='left')
        self.plotBtn0 = Button(self.controlFrm, text='Plot 0', command=lambda: self.plot(0))
        self.plotBtn0.pack()
        self.plotBtn1 = Button(self.controlFrm, text='Plot 1', command=lambda: self.plot(1))
        self.plotBtn1.pack()

        self.mainFrm = Frame(self)
        self.mainFrm.pack(expand=True, fill='both')
        self.values = []
        self.filter = []
        self.plots = []
        self.cnts = []
        self.ydata = [[], []]
        self.tdata = [[], []]
        for i in range(2):
            frame = LabelFrame(self.mainFrm, text='Sensor {}'.format(i), width=500)
            self.values.append(value_frame(frame))
            frame.grid(row=i, column=0, padx=10, pady=10)
            self.filter.append(filter())
            fig = plt.figure(figsize=(5,2))
            ax=fig.add_subplot(1,1,1)
            canvas=FigureCanvasTkAgg(fig, master=self.mainFrm)
            canvas.draw()
            canvas.get_tk_widget().grid(row=i, column=1)
            self.plots.append([fig, ax, canvas])
            self.cnts.append(0)

    def dataIn(self, sid, svalue):
        if sid in (0, 1):
            davg, dmed, dmin, dmax = self.filter[sid].put(svalue)
            self.cnts[sid] += 1
            if self.cnts[sid] >= 10:
                self.values[sid].dval.set(svalue)
                self.cnts[sid] = 0
                self.values[sid].davg.set(int(davg))
                self.values[sid].dmed.set(int(dmed))
                self.values[sid].dmin.set(int(dmin))
                self.values[sid].dmax.set(int(dmax))
                self.ydata[sid].append(davg)
                now = datetime.datetime.now()
                self.tdata[sid].append(now)
                shortit = False
                for i, t in enumerate(self.tdata[sid]):
                    if (now - t).total_seconds() > 60:
                        shortit = True
                    else:
                        break
                if shortit:
                    self.ydata[sid] = self.ydata[sid][i:]
                    self.tdata[sid] = self.tdata[sid][i:]
                self.after(100, lambda:self.plot(sid))

    def startStop(self):
        if self.startBtn['text'] == 'Start':
            self.startBtn['text'] = 'Stop'
            for i in range(2):
                self.filter[i].reset()
                self.ydata[i] = []
                self.tdata[i] = []
            self.datain = data_thread(fout=self.dataIn)
            self.datain.start()
        else:
            self.startBtn['text'] = 'Start'
            self.datain.stop()

    def plot(self, pid):
        if pid in (0, 1):
            fig, ax, canvas = self.plots[pid]
            ax.clear()
            ax.plot(self.tdata[pid], self.ydata[pid])
            ax.grid()
            canvas.draw()

    def kill(self):
        if self.startBtn['text'] == 'Stop':
            self.after(100, self.startStop)
        else:
            sys.exit()

if __name__ == "__main__":
    app = App()
    app.mainloop()
