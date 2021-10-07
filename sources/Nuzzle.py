from machine import Pin
import utime
from time import sleep

R1 = Pin(5, Pin.IN, Pin.PULL_UP)
R2 = Pin(16, Pin.IN, Pin.PULL_UP)
R3 = Pin(14, Pin.IN, Pin.PULL_UP)
R4 = Pin(15, Pin.IN, Pin.PULL_UP)
S1 = Pin(13, Pin.IN, Pin.PULL_UP)
S2 = Pin(4, Pin.IN, Pin.PULL_UP)
S3 = Pin(12, Pin.IN, Pin.PULL_UP)

while True:
    if not S1() and not R1():
        print("1")
        while not button():
            pass
            