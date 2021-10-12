from time import sleep
from machine import Pin

led = Pin(16, Pin.OUT)
while True:
    led(1)
    sleep(.5)
    led(0)
    sleep(.5)
    led(1)
    sleep(.5)
    led(0)
    sleep(.5)
    led(1)
    

    sleep(1)