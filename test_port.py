#!/usr/bin/python3

import serial

PORT = '/dev/ttyACM0'

with serial.Serial(port=PORT, timeout=1.0) as port:
    while True:
        line = port.readline()
        if line == b'':
            break
        splt = line.decode('ascii').strip().split(',')
        sid = int(splt[0])
        try:
            sval = int(splt[1])
        except:
            sval = None
        print(sid, sval)
