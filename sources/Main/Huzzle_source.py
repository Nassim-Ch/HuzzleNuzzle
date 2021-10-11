# PCD8544 (Nokia 5110) LCD sample for Raspberry Pi Pico
# Required library:
#   https://github.com/mcauser/micropython-pcd8544
# And this sample script is based on above repository.
# Used script from https://github.com/mcauser/MicroPython-ESP8266-Nokia-5110-Conways-Game-of-Life

#--- For all ---#
from machine import Pin, SPI, I2C
import utime
from time import sleep
import urandom
#--------------------#

#--- For LCD-Screen ---#
import pcd8544
spi = SPI(1,baudrate=2000000, polarity=0, phase=0)
cs = Pin(2) # CE to D4 (2)
dc = Pin(15) # DC to D8 (15)
rst = Pin(0) # RST to D3 (0)
# DIN to D7 (13)  # CLK to D5 (14)
lcd = pcd8544.PCD8544(spi, cs, dc, rst)
import framebuf
buffer = bytearray((lcd.height // 8) * lcd.width)
framebuf = framebuf.FrameBuffer1(buffer, lcd.width, lcd.height)
#--------------------#

#--- For Internet ---#
import network
from netvars import setNetVar, getNetVar, initNet
#--------------------#

#--- For Button ---#
button = machine.ADC(0)
counter = 0
#--------------------#

#--- For RGB-Sensor ---#
import tcs34725
i2c = I2C(scl=Pin(5), sda=Pin(4))
rgb_sensor = tcs34725.TCS34725(i2c)
rgb_sensor.active(False)
rgb_power = Pin(16,Pin.OUT, value=1)
#--------------------#

#--- Intergrated LEDs ---#
display_light = Pin(12, Pin.OUT, value=1) # BL to D6 (12) # DISPLAY LIGHT
bl_state = False
#--------------------#

current_game_state = " "
played_stoerungen = tuple()
color_tolerance = 70
rgb_text = ["R ", "G ", "B "]
game_text = ["G1", "G2"]
        
#--- METHODS ---#
def connectInternet():
    # Enter Internet information here
    ssid = "600cc"
    password = "6795@2697@18803"
    
    initNet(ssid, password)

#--- Screen Effects __   
def clearScreen():
    framebuf.fill(0)
    lcd.data(buffer)

#--- BL Effects __
def screenLight(new_bl_state):
    bl_state = new_bl_state
    display_light.value(bl_state)

def screenBlink(num_blink, speed):
    for i in range(num_blink):
        bl_state = False
        display_light.value(bl_state)
        sleep(speed)
        bl_state = True
        display_light.value(bl_state)
        sleep(speed)

#--- Text Effects __
def printText(text, x, y):
    framebuf.text(text, x, y, 1)
    lcd.data(buffer)
    
# INIT #
def init():
    clearScreen()
    connectInternet()
    screenLight(False)

#-- Waiting -->
def waitingForPlayer():
    clearScreen()
    print("Player offline")
    printText("Waiting", 0,0)
    printText("for admin", 0, 9)

#-- Color Methods -->
def get_scanned_color():
    logged_color = tcs34725.html_rgb(rgb_sensor.read(True))
    print("Read color: ", logged_color)
    return logged_color

def get_random_color():
    random_RGB = tuple()
    random_RGB = (urandom.getrandbits(8),urandom.getrandbits(8),urandom.getrandbits(8))
    return random_RGB

def is_same_color(scan_c, selected_c):
    is_same = False
    checked_rgb = [True, True, True]
    for i in range(len(scan_c)-1):
        if not (selected_c[i]-color_tolerance <= scan_c[i] <= selected_c[i]+color_tolerance):
          checked_rgb[i] = False
          continue
    
    if False in checked_rgb: is_same = False
    else: is_same = True
    
    return is_same
        

#--- Color Game Method >>
def color_game(num_game):
    setNetVar("0huzzle", num_game)
    current_game_state = num_game
    random_RGB = get_random_color()
    print("Search for color: ", random_RGB)
    scanned_color = 0
    clearScreen()
    printText("Find color",0,0)
    
    for i in range(3):
        printText(rgb_text[i] + str(random_RGB[i]),0,18+(i*9))
    
    while True:
        button_value = button.read_u16() / 65535
        if (button_value == 1):
            scanned_color = get_scanned_color()
            if is_same_color(scanned_color, random_RGB):
                setNetVar("0huzzle", "right")
                print("Right color")
                clearScreen()
                printText("Task",0,0)
                printText("success-",0,9)
                printText("fully",0,18)
                printText("completed!",0,27)
                screenBlink(3,1)
                return
            else:
                clearScreen()
                printText("Try again",0,0)
                for i in range(3):
                    printText(rgb_text[i] + str(random_RGB[i]),0,18+(i*9))
                    printText(str(scanned_color[i]),54,18+(i*9))

#--- Störungen Game Method >>>
def choose_stoerung():
    # random number > check if played before > if yes = roll again // if no = methodenaufruf
    return
                    
#--- Finish Game Method >>>
def finishGame():
    clearScreen()
    printText("Congrats!", 0,0)
    sleep(10)
    start()
    return

# CODE RUN #
def main():
    print("Starting Game")
    screenLight(True)
    setNetVar("0huzzle", "ready")
    
    waitVal = True
    while waitVal:
        nuzzle = getNetVar("0nuzzle")
        if nuzzle == "ready": # ready
            print("Player ready")
            waitVal = False
        else:
            waitingForPlayer()
            sleep(2)
        sleep(.5)
    clearScreen()
    print("Start")
    
    sleep(5)
    #--- First Color Game ---#
    color_game("G1")
    print("Next Game!")
    
    #--- Störungen ---#
    nuzzle = getNetVar("0nuzzle")
    if "right" in nuzzle:
        if "G3" in nuzzle:
            finishGame()
            setNetVars("0huzzle", "finish")
            return
        if any(x in nuzzle for x in game_text):
            choose_stoerung()
        
    
        
    
def start():
    setNetVar("0huzzle", "offline")
    while True:
        value = button.read_u16()
        value =  value // 65535
        counter_button = 0
        clearScreen()
        while value==1:
            print(counter_button)
            counter_button += 1
            screenBlink(1,0.2)
            clearScreen()
            printText("Restart?",10,0)
            printText("Hold 5s", 10,9)
            printText(str(counter_button), 39,22)
            sleep(1)
            if counter_button >= 5:
                main()
                reset = True
                return
            value = button.read_u16()
            value =  value // 65535

init()
setNetVar("0huzzle", "offline")
start()

