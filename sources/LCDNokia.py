# PCD8544 (Nokia 5110) LCD sample for Raspberry Pi Pico
# Required library:
#   https://github.com/mcauser/micropython-pcd8544
# And this sample script is based on above repository.

# Used script from https://gist.github.com/Akkiesoft/c72034f89b9aa6a3bedd4994bd51676a (Akkiesoft)

# Connections:
#   [pcd8544:pico(physical pin)]
#   Gnd: Pico GND (38)
#   BL : Pico 3V3 (36)
#   Vcc: Pico 3V3 (36)
#   Clk: Pico GP6 ( 9)
#   Din: Pico GP7 (10)
#   DC : Pico GP4 ( 6)
#   CE : Pico GP5 ( 7)
#   RST: Pico GP8 (11)

import pcd8544_fb
from machine import Pin, SPI
import utime

spi = SPI(1)
spi.init(baudrate=2000000, polarity=0, phase=0)
print(spi)
cs = Pin(2)
dc = Pin(15)
rst = Pin(0)

lcd = pcd8544_fb.PCD8544_FB(spi, cs, dc, rst)

import framebuf
buffer = bytearray((pcd8544_fb.HEIGHT // 8) * pcd8544_fb.WIDTH)
framebuf = framebuf.FrameBuffer(buffer, pcd8544_fb.WIDTH, pcd8544_fb.HEIGHT, framebuf.MONO_VLSB)

# fill(color)
framebuf.fill(1)
lcd.data(buffer)
utime.sleep(1)
framebuf.fill(0)
lcd.data(buffer)
utime.sleep(1)

# text(string, x, y, color)
framebuf.text('Hi Hanna', 0, 0, 1)
framebuf.text('init LCD', 0, 10, 1)
lcd.data(buffer)
utime.sleep(1)

# Smiley
def drawSmiley():
    framebuf.hline(10,25,10,1)

    framebuf.pixel(9,26,1)
    framebuf.pixel(20,26,1)

    framebuf.pixel(8,27,1)
    framebuf.pixel(21,27,1)

    framebuf.vline(7,28,5,1)
    framebuf.vline(22,28,5,1)

    framebuf.fill_rect(10, 28, 2, 2, 1)
    framebuf.fill_rect(17, 28, 2, 2, 1)

    framebuf.pixel(10,31,1)
    framebuf.pixel(19,31,1)
    framebuf.hline(11,32,8,1)

    framebuf.pixel(8,33,1)
    framebuf.pixel(21,33,1)

    framebuf.pixel(9,34,1)
    framebuf.pixel(20,34,1)

    framebuf.hline(10,35,10,1)

    lcd.data(buffer)
    utime.sleep(1)

drawSmiley()

#----- LCD Examples ------#
# pixel(x, y, colour)
#   framebuf.pixel(63, 20, 1)
#   lcd.data(buffer)
#   utime.sleep(1)

# line(x1, y1, x2, y2, color)
#   framebuf.line(67, 27, 83, 20, 1)
#   framebuf.line(83, 27, 67, 20, 1)
#   lcd.data(buffer)
#   utime.sleep(1)

# hline(x, y, w, color)
#   framebuf.hline(0, 30, 84, 1)
#   lcd.data(buffer)
#   utime.sleep(1)

# vline(x, y, h, color)
#   framebuf.vline(40, 0, 47, 1)
#   lcd.data(buffer)
#   utime.sleep(1)

# rect(x, y, w, h, c)
#   framebuf.rect(10, 32, 20, 16, 1)
#   lcd.data(buffer)
#   utime.sleep(1)

# fill_rect(x, y, w, h, c)
#   framebuf.fill_rect(50, 32, 20, 16, 1)
#   lcd.data(buffer)
#   utime.sleep(1)

# if your pcd8544 has BL pin, uncomment this line.
#   bl = Pin(28, Pin.OUT, value=0)
