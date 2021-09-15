from machine import Pin
import utime
from time import sleep

morseCode = True
led_r = Pin(16, Pin.OUT)
led_g = Pin(17, Pin.OUT)
led_b = Pin(15, Pin.OUT)
button = Pin(13, Pin.IN, Pin.PULL_DOWN)
code = [-1, -1, -1, -1, -1, -1, -1]
code_Counter = 0

while morseCode:
    
    pressed = False
    longPress = False
    press_Counter = 2
    while button.value():
        
        # alles soll leuchten (evtl. eine weiße LED einbauen?)
        led_r.value(1)
        led_g.value(1)
        led_b.value(1)
        
        pressed = True
        press_Counter -= 1
        sleep(.5)
        
    # bei Button loslassen aus (evtl. eine weiße LED einbauen?)
    # TODO bei kurzem Drücken, leuchtet es etwas länger, wegen sleep (aber das ist notwendig für den Button!)
    led_r.value(0)
    led_g.value(0)
    led_b.value(0)
        
    if press_Counter <= 0:
        longPress = True
    
    if pressed:
        if longPress:
            code[code_Counter] = 1
        else:
            code[code_Counter] = 0
        code_Counter += 1
    
    if code_Counter >= len(code):
        if code == [0, 1, 1, 0, 0, 0, 1]:
            morseCode = False
            
        else:
            code = [-1, -1, -1, -1, -1, -1, -1]
            code_Counter = 0
            i = 0
            while i < 3:   # eventuell auch einmal kurz rot aufleuchten, statt dreimal blinken?
                led_r.value(1)
                sleep(.5)
                led_r.value(0)
                sleep(.5)
                i += 1

# nach richtigem Lösen

# eventuell eine Grünge LED am rand aktivieren über led_lsgMorse.value(1)
notEntered = True

while notEntered:
    led_b.value(1)
    sleep(1)
    led_b.value(0)
    led_g.value(1)
    sleep(1)
    led_g.value(0)
    led_b.value(1)
    sleep(1)
    led_b.value(0)
    led_r.value(1)
    sleep(1)
    led_r.value(0)
    sleep(2.5)

