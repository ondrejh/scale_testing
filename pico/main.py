''' rpi pico program (micropython):
Reads 2 hx711 ADCs and sends data to debug output.
Uses my own hx711 class to read data - simple bitbanging.
'''

from machine import Pin
from utime import sleep_us, sleep, ticks_ms

ERR_TIMEOUT = 500 # ms .. how long to wait when readout is not valid

# adc 0 pinout
DI1 = Pin(16, Pin.IN, pull=Pin.PULL_DOWN)
CLK1 = Pin(18, Pin.OUT)
# adc 1 pinout
DI2 = Pin(15, Pin.IN, pull=Pin.PULL_DOWN)
CLK2 = Pin(13, Pin.OUT)

# hx711 ADC class
class hx711:
    def __init__(self, clk, di, err_timeout=ERR_TIMEOUT):
        self.di = Pin(di, Pin.IN, pull=Pin.PULL_DOWN)
        self.clk = Pin(clk, Pin.OUT)
        self.err = False
        self.ticks = 0
        self.timeout = err_timeout

    def ready(self):
        if self.err:
            if ticks_ms() - self.ticks >= self.timeout:
                self.err = False
            else:
                return False
            
        return self.di.value() == False

    def read(self):
        val = 0
        # read 24 bits, msb first
        for i in range(24):
            val *= 2
            self.clk.value(1)
            self.clk.value(0)
            if self.di.value() == True:
                val += 1

        # send 25th clk to finish
        self.clk.value(1)
        self.clk.value(0)

        # if still false, something is wrong (most likely its not connected)
        if self.di.value() == False:
            self.ticks = ticks_ms()
            self.err = True
            return None

        # if fist bit was 1 its negative
        if (val & (1<<23)) != 0:
            val -= (1<<24)
        
        return val

# create ACD instances
myhx = []
myhx.append(hx711(clk=18, di=16))
myhx.append(hx711(clk=13, di=15))

# read and print when acd is ready
while True:
    for i in range(2):
        if myhx[i].ready():
            val = myhx[i].read()
            if val is not None:
                print('{},{}'.format(i, val))
