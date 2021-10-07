
from machine import Pin, sleep
import board
import adafruit_tcs34725

i2c_sensor = board.I2C()
rgb_sensor = adafruit_tcs34725.TCS34745(i2c)

led_red = Pin(15, Pin.OUT)
led_blue = Pin(13, Pin.OUT)
led_green = Pin(12, Pin.OUT)

BLUE = "blue"
GREEN = "green"
RED = "red"
MAGENTA = "magenta"
CYAN = "cyan"
YELLOW = "yellow"

def init():
    led_red.off()
    led_green.off()
    led_blue.off()

def showColor(color):
    init()
    
    if color == BLUE:
        led_blue.on()
    elif color == GREEN:
        led_green.on()
    elif color == RED:
        led_red.on()
    elif color == MAGENTA:
        led_red.on()
        led_blue.on()
    elif color == CYAN:
        led_blue.on()
        led_green.on()
    elif color == YELLOW:
        led_red.on()
        led_green.on()
    
init()

while True:
    showColor(BLUE)
    sleep(500)
    showColor(GREEN)
    sleep(500)
    showColor(RED)
    sleep(500)
    showColor(MAGENTA)
    sleep(500)
    showColor(CYAN)
    sleep(500)
    showColor(YELLOW)
    sleep(500)

    
    