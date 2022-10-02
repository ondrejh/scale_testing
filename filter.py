#!/bin/python3

from data_thread import data_thread

class filter:
    def __init__(self, flen=64):
        self.flen = flen
        self.first = True
        self.data = [0] * self.flen
        self.dptr = 0
        self.dmed = 0
        self.dmin = 0
        self.dmax = 0
        self.davg = 0
    def put(self, value):
        #print(value)
        if self.first:
            self.first = False
            for i in range(self.flen):
                self.data[i] = value
            self.dmed = self.dmin = self.dmax = self.davg = value
        else:
            self.data[self.dptr] = value
            self.dmin = min(self.data)
            self.dmax = max(self.data)
            davg = 0
            data_med = [0] * self.flen
            for i in range(self.flen):
                davg += self.data[i]
                data_med[i] = self.data[i]
            davg /= self.flen
            self.davg = davg
            data_med.sort()
            self.dmed = data_med[self.flen // 2]
            self.dptr += 1
            if self.dptr >= self.flen:
                self.dptr = 0
        return self.davg, self.dmed, self.dmin, self.dmax
    def reset(self):
        self.data = [0] * self.flen
        self.dptr = 0
        self.first = True
        self.dmed = self.davg = self.dmin = self.dmax = 0


data = {}

def data_in(sid, svalue):
    strid = str(sid)
    intval = int(svalue)
    if strid not in data.keys():
        data[strid] = {}
        data[strid]['filter'] = filter()
        data[strid]['counter'] = 0
    fltr = data[strid]['filter']
    data[strid]['counter'] += 1
    davg, dmed, dmin, dmax = fltr.put(intval)
    if data[strid]['counter'] >= 10:
        data[strid]['counter'] = 0
        print(sid, svalue, davg, dmed, dmin, dmax)

def dprint(sid, svalue):
    print(sid, svalue)

if __name__ == "__main__":
    dtt = data_thread(fout=data_in)
    dtt.start()
