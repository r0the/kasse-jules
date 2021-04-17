import display
import time
import keypad

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

text = ""

def input_number():
    global text
    modified = False
    for key in keypad.pressed():
        text = text + key
        modified = True
    if modified:
        display.clear()
        display.text(10, 0, "Kasse")
        display.text(10, 60, "Version 0.2")
        display.text(10, 120, text)
        display.show(fast=True)

def main():
    display.clear()
    display.text(10, 0, "Kasse")
    display.text(10, 60, "Version 0.2")
    display.show(fast=False)   
    while True:
        keypad.poll()
        input_number()
#        time.sleep(0.2)

if __name__ == '__main__':
    main()
