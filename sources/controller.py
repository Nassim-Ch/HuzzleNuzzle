# ------ Controller Class ------ #
# Use this class for
#  -Communication between view and model
#  -receiving user input and processing
#  -internet connection

# How to prepare Internet
# -Select Micropython (ESP32)
# -Enter correct ssid and password

import network
from netvars import setNetVar, getNetVar, initNet
import time
import mcp23017
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
    
def setupExpanders():
    i2c_1 = I2C(scl=Pin(14), sda=Pin(12))
    #i2c_2 = I2C(scl=Pin(14), sda=Pin(12))
    #i2c_3 = I2C(scl=Pin(0), sda=Pin(2))
    print("I2C_1: ", i2c_1.scan())
    mcp_1 = mcp23017.MCP23017(i2c_1, 0x20)
   # mcp_2 = mcp23017.MCP23017(i2c_1, 0x21)
    #mcp_3 = mcp23017.MCP23017(i2c_1, 0x22)
    
    #mcp_1[7].output()
    
    #mcp_1[7].value(1)
    #sleep(1)
    
    #mcp[7].value(0)
    #sleep(1
    mcp_1[9].output(1)  # GPA7: mcp_x[7].output(1), GPB0: mcp_x[8].output(1)
   # mcp_1.porta.gpio = 0x40
    
# initialize cube
def init():
  #  connectInternet()
    setupExpanders()
    #setNetVar("HuzzleNuzzle", "Test")
    
#while True:
init()
    
