# PCD8544 (Nokia 5110) LCD sample for Raspberry Pi Pico
# Required library:
#   https://github.com/mcauser/micropython-pcd8544
# And this sample script is based on above repository.

# Used script from https://github.com/mcauser/MicroPython-ESP8266-Nokia-5110-Conways-Game-of-Life

#--- For LCD-Screen ---#
import pcd8544
from machine import Pin, SPI
import utime
spi = SPI(1,baudrate=80000000, polarity=0, phase=0)
cs = Pin(2) # CE to D4 (2)
dc = Pin(15) # DC to D8 (15)
rst = Pin(0) # RST to D3 (0)
bl = Pin(12, Pin.OUT, value=1) # BL to D6 (12)
# DIN to D7 (13)  # CLK to D5 (14)
lcd = pcd8544.PCD8544(spi, cs, dc, rst)
import framebuf
buffer = bytearray((lcd.height // 8) * lcd.width)
framebuf = framebuf.FrameBuffer1(buffer, lcd.width, lcd.height)

#--- For Internet ---#
import network
from netvars import setNetVar, getNetVar, initNet
import time
from machine import Pin, I2C

#def startGame():
    # start Screen
    # get Internet connection
    # if true
        # get waiting time
        # get game round mit getNetVar(key, value)
        # set view
        # set model(gameround)

def connectInternet():
    # Enter Internet information here
    ssid = "600cc"
    password = "6795@2697@18803"
    
    initNet(ssid, password)
    
def clearScreen():
    framebuf.fill(0)
    lcd.data(buffer)
    
# initialize cube
#def init():
  #  connectInternet()

    #setNetVar("HuzzleNuzzle", "Test")
    
#while True:
#init()