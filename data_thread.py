#!/usr/bin/python3

import serial
import threading
from time import sleep

PORT = '/dev/ttyACM0'


class data_thread(threading.Thread):
    ''' The tread reads data from serial 'port' and two intergers
    separated by ',' found, it's passed to function 'fout' as its 
    arguments. '''

    def __init__(self, port=PORT, fout=print):
        threading.Thread.__init__(self)
        self.port_name = port
        self.output_function = fout
        self.stopped = False
    def run(self):
        with serial.Serial(port=self.port_name, timeout=1.0) as port:
            while not self.stopped:
                line = port.readline()
                try:
                    splt = line.decode('ascii').strip().split(',')
                    sid = int(splt[0])
                    sval = int(splt[1])
                except:
                    sleep(0.1)
                    continue
                self.output_function(sid, sval)
    def stop(self):
        self.stopped = True


# test it
if __name__ == '__main__':

    din = data_thread(PORT, print)
    din.start()

