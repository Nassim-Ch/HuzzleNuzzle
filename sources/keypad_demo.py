from machine import Pin
from time import sleep

# CONSTANTS
KEY_UP   = const(1)
KEY_DOWN = const(0)
last_key_press = -1

keys = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9'], ['*', '0', '#']]

# Pin names for Pico
rows = [0, 2, 13, 12]
cols = [5, 4, 14]


# set pins for rows as outputs
row_pins = [Pin(pin_name, mode=Pin.OUT) for pin_name in rows]

# set pins for cols as inputs
col_pins = [Pin(pin_name, mode=Pin.IN, pull=Pin.PULL_UP) for pin_name in cols]

def init():
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

print("starting")

# set all the columns to low
init()
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
            pressed = -1
            pressArr = [-1, -1, -1, -1]
            
    sleep(.05)