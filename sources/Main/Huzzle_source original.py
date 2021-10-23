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
import time
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
played_stoerungen = []
played_colorgames = []
color_tolerance = 70
rgb_text = ["R ", "G ", "B "]
game_text = ["G1", "G2"]
countdown_time = 10

#--- pictures ---#
party_f1 = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
[0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0],
[0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,1,1,0,0,1,1,0,0,0,1,0,0,0],
[0,0,0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0],
[0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0],
[0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0],
[0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0],
[0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0],
[0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0],
[0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0],
[0,0,0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0],
[0,0,1,0,0,1,0,0,0,1,1,0,0,0,0,0,1,0,1,0],
[0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0],
[0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
party_f2 = [
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,1,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0],
[0,0,0,1,1,0,0,0,0,0,1,1,0,0,0,0,1,0,0,0],
[0,0,0,1,1,0,0,0,1,1,0,0,1,1,0,0,0,1,0,0],
[0,0,1,0,0,1,0,0,1,1,0,0,1,1,0,0,1,0,0,0],
[0,0,0,0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0],
[0,0,0,0,1,1,1,1,0,0,0,0,0,0,1,1,1,1,0,0],
[0,0,0,0,1,1,1,1,0,0,0,0,0,0,1,1,1,1,0,0],
[0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
[0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
[0,0,0,0,1,1,1,1,0,0,0,0,0,0,1,1,1,1,0,0],
[0,0,0,0,1,1,1,1,0,0,0,0,0,0,1,1,1,1,0,0],
[0,0,0,0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,1,1,0,0,1,1,0,0,0,1,0,0],
[0,0,0,1,1,0,0,0,1,1,0,0,1,1,0,0,1,0,1,0],
[0,0,0,1,1,0,0,0,0,0,1,1,0,0,0,0,0,1,0,0],
[0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

#--- METHODS ---#
def connectInternet():
    # Enter Internet information here
    #ssid = "600cc"
    #password = "6795@2697@18803"
    ssid = "AndroidAP"
    password = "nana6795"
    
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

#--- Networking Methods >>
def sendToNet(message):
    setNetVar("0huzzle", str(message))
    print("Sent to network: ", str(message))

#--- Color Game Method >>
def color_game(num_game):
    sendToNet(num_game)
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
                sendToNet("right")
                print("Right color")
                clearScreen()
                printText("Task",0,0)
                printText("success-",0,9)
                printText("fully",0,18)
                printText("completed!",0,27)
                screenBlink(3,1)
                played_colorgames.append(num_game)
                return
            else:
                clearScreen()
                printText("Try again",0,0)
                for i in range(3):
                    printText(rgb_text[i] + str(random_RGB[i]),0,18+(i*9))
                    printText(str(scanned_color[i]),54,18+(i*9))

#--- Störungen Game Method >>>
def get_rand_s():
    rand_stoerung = urandom.getrandbits(2)
    
    while rand_stoerung in played_stoerungen:
        rand_stoerung = urandom.getrandbits(2)
    return rand_stoerung

def draw_timeline(prev_time, elapsed_time):
    if time.time()-prev_time >= 1:
        prev_time = time.time()
        framebuf.fill_rect(0,43,8*elapsed_time,5,1)
        lcd.data(buffer)
        elapsed_time+=1
    return prev_time, elapsed_time
    
def stoer_1_colorgame(): # TODO: implement timer and ticking
    random_RGB = get_random_color()
    print("Search for color: ", random_RGB)
    scanned_color = 0
    clearScreen()
    printText("Find color!",0,0)
    prev_time = 0
    elapsed_time = 0
    
    for i in range(3):
        printText(rgb_text[i] + str(random_RGB[i]),0,18+(i*9))
    while True:
        button_value = button.read_u16() / 65535
        if (button_value == 1):
            scanned_color = get_scanned_color()
            if is_same_color(scanned_color, random_RGB):
                print("Right color")
                clearScreen()
                printText("System",0,0)
                printText("stable",0,9)
                screenBlink(3,1)
                return
            else:
                if elapsed_time >= countdown_time:
                  random_RGB = get_random_color()
                  elapsed_time = 0
                clearScreen()
                prev_time, elapsed_time = draw_timeline(prev_time, elapsed_time)
                printText("Try again",0,0)
                for i in range(3):
                    printText(rgb_text[i] + str(random_RGB[i]),0,18+(i*9))
                    printText(str(scanned_color[i]),54,18+(i*9))
    
    
def play_stoerung_1(): # Hackerkonsole fällt aus
    clearScreen()
    current_game_state = "S1"
    sendToNet("S1")
    while current_game_state is "S1":
        printText("Error 401",0,0)
        printText("4x00932",0,9)
        printText("waiting...",0,18)
        screenBlink(3,1)
        
        if getNetVar("0nuzzle") is "SOS":
            clearScreen()
            stoer_1_colorgame()
            sendToNet("rightS1")
            sleep(30)
            sendToNet("G" + len(played_colorgames)) 
            return
    return

def blink_display_morse(morsecode):
    for x in morsecode:
        screenBlink(x, 0.5)
    sleep(1)
    
def play_stoerung_2(): # Würfel von Agent fällt aus
    clearScreen()
    current_game_state = "S2"
    sendToNet("S2")
    morsecode = (1,5,1,3)
    
    while current_game_state is "S2":
        printText("System",0,0)
        printText("Shutdown",0,9)
        printText("Call admin",0,27)
        blink_display_morse(morsecode)
        
        if getNetVar("0nuzzle") is "rightS2":
            clearScreen()
            printText("Reboot",0,0)
            screenBlink(3,1)
            sleep(3)
            return
    return

def init_S3():
    framebuf.text("Connection", 0,0, 1)
    framebuf.text("failed x", 0,9, 1)
    framebuf.text("0 8 9 5 6", 0,18, 1)
    framebuf.text("2 * 3 1 7", 0,27, 1)
    framebuf.text("3    9", 0,36, 1)
    lcd.data(buffer)
    sleep(1)
    return

def random_lines(amount):
    for x in range(amount):
        framebuf.hline(0, urandom.getrandbits(6), 84, 0)
        
def random_pixel(amount):
    for x in range(amount):
        framebuf.pixel(urandom.getrandbits(7), urandom.getrandbits(6),1)
        
def play_stoerung_3(): # Verbindungsabbruch
    clearScreen()
    current_game_state = "S3"
    sendToNet("S3")
    
    init_S3()
    
    while current_game_state is "S3":
        framebuf.text("Connection", 0,0, 1)
        framebuf.text("failed x", 0,9, 1)
        framebuf.text("0 8 9 5 6", 0,18, 1)
        framebuf.text("2 * 3 1 7", 0,27, 1)
        framebuf.text("3    9", 0,36, 1)
        random_lines(40)
        random_pixel(40)
        lcd.data(buffer)
        sleep(urandom.getrandbits(3)/10)
        
        nuzzle = getNetVar("0nuzzle")
        if "right" in nuzzle:
            clearScreen()
            printText("Establish", 0,0)
            printText("connection", 0,9)
            printText(".",0,18)
            sleep(0.5)
            printText("..",0,18)
            sleep(0.5)
            printText("...",0,18)
            sleep(0.5)
            clearScreen()
            printText("Success-", 0,0)
            printText("fully", 0,9)
            printText("connected!",0,18)
            screenBlink(3,1)
            sleep(3)
            return
        
    return

def scan_light():
    while True:
        button_value = button.read_u16() / 65535 
        if (button_value == 1):
            if rgb_sensor.read(False)[0] >= 4000:
                print("Enough energy")
                clearScreen()
                printText("Admin",0,0)
                printText("reconnected",0,9)
                screenBlink(3,1)
                return
            else:
                printText("Try again!",0,44)
                screenBlink(2,0.2)
    
def play_stoerung_4(): # Stromausfall
    clearScreen()
    current_game_state = "S4"
    sendToNet("S4")
    
    while current_game_state is "S4":
        printText("Error",0,0)
        printText("010000010101001",0,9)
        printText("Wait for",0,27)
        printText("response",0,36)
        
        if getNetVar("0nuzzle") is "SOS":
            clearScreen()
            printText("Admin",0,0)
            printText("pwr loss",0,9)
            printText("Send pwr!",0,27)
            scan_light()
            sendToNet("rightS4")
            return
    return

def choose_stoerung():
    # random number > check if played before > if yes = roll again // if no = methodenaufruf
    # make random number <2
    rand_stoerung = get_rand_s()
    
    # check if already played
    if rand_stoerung not in played_stoerungen:
        sendToNet("S" + str(rand_stoerung))
        if rand_stoerung == 0:
            play_stoerung_1()
        elif rand_stoerung == 1:
            play_stoerung_2()
        elif rand_stoerung == 2:
            play_stoerung_3()
        elif rand_stoerung == 3:
            play_stoerung_4()
        played_stoerungen.append(rand_stoerung)
        return
    else:
        print("Cannot find right Stoerung...")
     

#--- Finish Game Method >>>
def display_party_anim(x_spawn,y_spawn):
    framebuf.fill_rect(0,9,84,48,0)
    lcd.data(buffer)
    for i in range(2):
        framebuf.fill_rect(0,9,84,48,0)
        lcd.data(buffer)
        for x in range(20):
            for y in range(20):
                if i == 0:
                    if party_f1[x][y] == 1:
                        framebuf.pixel(x+x_spawn,y+y_spawn,1)
                elif i == 1:
                    if party_f2[x][y] == 1:
                        framebuf.pixel(x+x_spawn,y+y_spawn,1)
        lcd.data(buffer)
        sleep(0.5)
        
def finishGame():
    clearScreen()
    printText("Congrats!", 0,0)
    for i in range(10):
        display_party_anim(0,10)
        display_party_anim(22,10)
        display_party_anim(44,10)
    start()
    return

# CODE RUN #
def main():
    print("Starting Game")
    screenLight(True)
    sendToNet("ready")
    
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
    
    #--- Störung 1 ---#
    while True:
        sleep(1)
        nuzzle = getNetVar("0nuzzle")
        if "right" in nuzzle:
            if any(x in nuzzle for x in game_text):
                choose_stoerung()
                break
     
    #--- Second Color Game ---#
    color_game("G2")
    print("Next Game!")
    
    #--- Störung 2 ---#
    while True:
        nuzzle = getNetVar("0nuzzle")
        if any(x in nuzzle for x in game_text):
            choose_stoerung()
            break
    
    #--- Störung 3 ---#
    while True:
        nuzzle = getNetVar("0nuzzle")
        if any(x in nuzzle for x in game_text):
            choose_stoerung()
            break
    
    #--- Third Color Game ---#
    color_game("G3")
    
    #--- Finish ---#
    print("Finish Game!")
    finishGame()
    sleep(30)
    sendToNet("offline")
    
    return
        
    
def start():
    sendToNet("offline")
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
sendToNet("offline")
start()