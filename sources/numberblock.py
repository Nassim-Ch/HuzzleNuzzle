from machine import Pin
import utime
from time import sleep

Dock1 = Pin(5, Pin.OUT)
Dock2 = Pin(2, Pin.IN, Pin.PULL_DOWN)


while True:
    Dock1.high()
    print("1:", Dock1.value())
    print("2:", Dock2.value())
    sleep(1)
