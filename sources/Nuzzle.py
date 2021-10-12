from machine import Pin
from time import sleep
import neopixel
from netvars import setNetVar, getNetVar, initNet

# Enter Internet information here
ssid = "FRITZ!Box 7430 OK"
password = "51469301520720766550"

initNet(ssid, password)
# initial all Nuzzle Objects

led = Pin(16, Pin.OUT)
button = machine.ADC(0)
np = neopixel.NeoPixel(machine.Pin(15), 12)
n = np.n
rows = [0, 2, 13, 12]
cols = [5, 4, 14]

KEY_UP   = const(1)
KEY_DOWN = const(0)
keys = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9'], ['*', '0', '#']]

row_pins = [Pin(pin_name, mode=Pin.OUT) for pin_name in rows]
col_pins = [Pin(pin_name, mode=Pin.IN, pull=Pin.PULL_UP) for pin_name in cols]

for row in range(0,4):
        for col in range(0,3):
            row_pins[row].off()
    
def scan(row, col):
    """ scan the keypad """

    # set the current column to high
    row_pins[row].on()
    key = None

    # check for keypressed events
    if col_pins[col].value() == KEY_DOWN:
        key = KEY_DOWN
    if col_pins[col].value() == KEY_UP:
        key = KEY_UP
    row_pins[row].off()

    # return the key state
    return key
   
def start():
    setNetVar("0nuzzle", "offline")
    while True:
        value = button.read_u16()
        value =  value // 65535
        counter_button = 0
        while value:
            print(counter_button)
            counter_button += 1
            sleep(1.5)
            if counter_button >= 5:
                main()
                return
            value = button.read_u16()
            value =  value // 65535
            
    
    
# Neon Pixel
def clear():
    for i in range(n):
        np[i] = (0, 0, 0)
    np.write()

def colour(r, g, b):
    for i in range(n):
        np[i] = (r, g, b)
    np.write()
    
def cycle(r, g, b):
    for i in range(n):
        for j in range(n):
            np[j] = (0, 0, 0)
        np[i % n] = (r, g, b)
        np.write()
        sleep(.4)
        
def speedCycle(r, g, b):
    for i in range(n):
        for j in range(n):
            np[j] = (0, 0, 0)
        np[i % n] = (r, g, b)
        np.write()
        sleep(.05)
        
def fadeInOut():
    for i in range(0, 4 * 256, 12):
        for j in range(n):
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
            np[j] = (val, val, val)
        np.write()
        sleep(.02)

def falseCode(gx):
    print("ToDo")
    
def correctCode(gx):
    print("correctCode")
    colour(180, 180, 180)
    led(0)
    code = "0"
    sleep = 0
    if gx == 1:
        code = "2412"
        sleep = 0.3
    elif gx == 2:
        code = "5375"
        sleep = 0.2
    elif gx == 3:
        code = "9638"
        sleep = 0.1
    if code == "0":
        print("kein Code")
        
    buttonVal = morse(code, sleep)
    print("morse ende")
    if buttonVal:
        setNetVar("0nuzzle", "wrong")
    else:
        butVal = True
        print("button press needed")
        while butVal:
            value = button.read_u16()
            value =  value // 65535
            if value == 1:
                print("korrekt")
                setNetVar("0nuzzle", "rightG"+str(gx))
                butVal = False
                
    
def morse(code, sleepNum):
    print("morse")
    valCode = True
    while valCode:
        colour(180, 180, 0)
        led(0)
        sleep(.3)
        blink(code, sleepNum)
        colour(180, 180, 180)
        inputCode = keypad(4, True)
        codeArr = [-1] * len(code)
        for i in range(len(code)):
            codeArr[i] = code[i]
        if inputCode == codeArr:
            valCode = False
            speedCycle(0, 180, 0)
            colour(0, 180, 0)
            led(1)
            return False
        else:
            speedCycle(180, 0, 0)
            colour(180, 0, 0)
           # for i in range(5):
           #     value = button.read_u16()
           #     value =  value // 65535
           #     if value == 1:
           #         return True
            sleep(.5)
            
            

def blink(num, sleepNum):
    print("blink")
    for i in range(2):
        for i in range(int(len(num))):
            sleep(2*sleepNum)
            for j in range(int(num[i])):
                led(1)
                sleep(sleepNum)
                led(0)
                sleep(sleepNum)
        sleep(4*sleepNum)
         
   
def keypad(num, game):
    last_key_press = -1
    code = [-1]*num
    code_count = 0
    pressed = -1
    pressArr = [-1, -1, -1, -1]
    i = 0
    while True:
        for row in range(4):
            for col in range(3):
                key = scan(row, col)
                if key == KEY_DOWN:
                    pressed = col
                    pressArr[row] = row
            if pressed != -1 and row not in pressArr:
                   
                if pressArr.count(-1) == 1 and last_key_press != keys[row][pressed]:
                    print("Key Pressed", keys[row][pressed])
                    last_key_press = keys[row][pressed]
                    
                    if last_key_press == '#':
                        code = [-1]*num
                        code_count = 0
                        print(code)
                        print(code_count)
                        
                        if game:
                            speedCycle(0, 0, 180)
                            colour(0, 0, 180)
                            colour(180, 180, 180)
                        else:
                            speedCycle(180, 0, 0)
                            colour(180, 0, 0)

                    else:
                        code[code_count] = last_key_press
                        if game:
                            np[code_count] = (0, 0, 180)
                            np.write()
                        else:
                            np[code_count] = (64, 64, 64)
                            np.write()
                        code_count += 1
                        print("code", code)
                        if code_count >= num:
                            print(code)
                            return code
                    
                    
                pressed = -1
                pressArr = [-1, -1, -1, -1]
            
        sleep(.05)

def gameCode(gx):
    print("gameCode")
    waitVal = True
    while waitVal:
       cycle(0, 0, 180)
       #huzzle = getNetVar("0huzzle")
       huzzle = "right"
       if huzzle == "right": # beginsWith
            correctCode(gx)
            waitVal = False
            break
       elif huzzle == "wrong":
            falseCode(gx)
            waitVal = False
            break

def alarmBlink():
    speedCycle(180,0,0)
    colour(180,0,0)
    sleep(.2)
    colour(180,0,0)

def waitSOS():
    waitVal = True
    while waitVal:
       cycle(180, 0, 0)
       #huzzle = getNetVar("0huzzle")
       huzzle = "rightS1"
       if huzzle == "rightS1": # beginsWith
            waitVal = False
            colour(180, 180, 180)
            break

def waitSOSVier():
    waitVal = True
    while waitVal:
       cycle(3, 3, 3)
       #huzzle = getNetVar("0huzzle")
       huzzle = "rightS4"
       if huzzle == "rightS4": # beginsWith
            waitVal = False
            colour(180, 180, 180)
            break
    
def stoerrungEinsVier(sx):
    print("stoerrung Eins/Vier: ", sx)
    shortOne = 0
    shortTwo = 0
    long = 0
    sosCount = 0
    sosVal = True
    if sx == 1:
        led(0)
        for i in range(4):
            alarmBlink()
    elif sx == 4:
        for i in range(0, 256, 12):
            for j in range(n):
                val = i & 0xff
                np[j] = (val, val, val)
                np.write()
        sleep(.05)
        led(0)
        for i in range(0, 256, 12):
            for j in range(n):
                val = 255 - (i & 0xff)
                np[j] = (val, val, val)
            np.write()
            sleep(.02)
            
    while sosVal:
        led(0)
        value = button.read_u16()
        value =  value // 65535
        counter_button = 0
        noAction = True
        while value:
            print("counter_button", counter_button)
            led(1)
            counter_button += 1
            sleep(.3)
            value = button.read_u16()
            value =  value // 65535
        led(0)
        if counter_button >= 3:
            if sosCount == 1 and long <= 3:
                noAction = False
                print("long")
                long += 1
                if sx == 1:
                    np[shortOne+shortTwo+long] = (64, 64, 64)
                elif sx == 4:
                    np[shortOne+shortTwo+long] = (0, 0, 0)
                np.write()
                if long == 3:
                    sosCount = 3
        elif counter_button > 0:
            if sosCount == 0 and shortOne <= 3:
                noAction = False
                print("short1")
                shortOne += 1
                if sx == 1:
                    np[shortOne+shortTwo+long] = (64, 64, 64)
                elif sx == 4:
                    np[shortOne+shortTwo+long] = (0, 0, 0)
                np.write()
                print(shortOne)
                if shortOne == 3:
                    sosCount = 1
            elif sosCount == 3 and shortTwo<= 3:
                noAction = False
                print("short2")
                shortTwo += 1
                if sx == 1:
                    np[shortOne+shortTwo+long] = (64, 64, 64)
                elif sx == 4:
                    np[shortOne+shortTwo+long] = (0, 0, 0)
                np.write()
                if shortTwo == 3:
                    finish = True
                    sosVal = False
                    break
              
        if noAction and counter_button > 0:
            print("wrong button")
            shortOne = 0
            shortTwo = 0
            long = 0
            sosCount = 0
            if sx == 1:
                alarmBlink()
            elif sx == 4:
                speedCyrcle(0,0,0)
                colour(3,3,3)             
    
    print("SOS eingegeben")
    colour(0,180,0)
    sleep(1)
    if sx == 1:
        led(1)
        waitSOS()
    elif sx == 4:
        waitSOSVier()
        led(1)
            
def stoerrungZweiDrei(code):
    print("stoerrung Zwei/Drei: ", code)
    led(0)
    for i in range(4):
        alarmBlink()
    valCode = True
    while valCode:
        colour(180, 0, 0)
        inputCode = keypad(len(code), False)
        if inputCode == code:
            valCode = False
            speedCycle(0, 180, 0)
            colour(0, 180, 0)
            led(1)
            break
        else:
            speedCycle(180, 0, 0)
            colour(180, 0, 0)
            sleep(.5)
    # press button
    butVal = True
    print("button press needed")
    while butVal:
        value = button.read_u16()
        value =  value // 65535
        if value == 1:
            print("korrekt")
            led(1)
            if len(code) == 4:
                setNetVar("0nuzzle", "rightS2")
            else:
                setNetVar("0nuzzle", "rightS3")
            butVal = False
            break
    
    
def stoerrung(sx):
    print("stoerrung")
    waitVal = True
    while waitVal:
        cycle(0, 0, 180)
        #huzzle = getNetVar("0huzzle")
        huzzle = "right"
        if sx == 1 or sx == 4:
            stoerrungEinsVier(sx)
            waitVal = False
            break
        elif sx == 2:
            stoerrungZweiDrei(['1','5','1','3'])
            waitVal = False
            break
        elif sx == 3:
            stoerrungZweiDrei(['0','8','9','5','6','2','*','3','1','7','3','9'])
            waitVal = False
            break


def decideGameState():
    print("GameState")
    # colour(180, 180, 180)
    waitVal = True
    while waitVal:
       # huzzle = getNetVar("0huzzle")
        huzzle = "S4"
        if huzzle.startswith("G"):
            gameCode(int(huzzle[1]))
            waitVal =False
            return
        elif huzzle.startswith("S"):
            stoerrung(int(huzzle[1]))
            waitVal = False
            return
        cycle(0, 0, 180)

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) 


def rainbow_cycle(speed):
    for i in range(12):
        pixel_index = (i * 256 // 12)
        np[i] = wheel(pixel_index & 255)
        np.write()
        sleep(speed)
        
def main():
    fadeInOut()
    led(1)
    setNetVar("0nuzzle", "ready")
    waitVal = True
    while waitVal:
        #huzzle = getNetVar("0huzzle")
        huzzle = "ready"
        if huzzle == "ready":
            waitVal = False
        else:
            cycle(0, 0, 180)
        sleep(.5)  
    # 1. Game
  #  for i in range(4):  #an sich 4
  #      decideGameState()
  #      print("Game finish")
  #      fadeInOut()
    
    # fin
    rainbow_cycle(.07)
    colour(3, 3, 3)
    rainbow_cycle(.02)
    colour(3, 3, 3)
    rainbow_cycle(.09)
    colour(3, 3, 3)
    rainbow_cycle(.03)
    colour(3, 3, 3)
    rainbow_cycle(.05)
    colour(3, 3, 3)
    for i in range(0, 256, 12):
            for j in range(12):
                val = i & 0xff
                np[j] = (val, val, val)
                np.write()
    sleep(.1)
    colour(0,0,0)
    led(0)
    setNetVar("0nuzzle", "offline")
    
    
#start()
main()
# start()
