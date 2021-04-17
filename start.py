#!/usr/bin/python3
import camera
import display
import time
import keypad
import subprocess

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

MENU_KEY_X = 10
MENU_TEXT_X = 50

def power_off():
    subprocess.call("sudo poweroff")

def register():
    display.clear()
    display.text(10, 0, "Kasse")
    display.show()
    global text
    while True:
        keypad.poll()
        modified = False
        for key in keypad.pressed():
            if key == "*":
                return "main_menu"
            text = text + key
            modified = True
        if modified:
            display.clear()
            display.text(MENU_KEY_X, 0, "Kasse")
            display.rectangle(10, 120, 380, 55)
            display.text(10, 120, text)
            display.show(fast=True)


def show_menu(menu):
    display.clear()
    y = 0
    for entry in menu:
        display.text(MENU_KEY_X, y, entry[0])
        display.text(MENU_TEXT_X, y, entry[1])
        y = y + 50
    display.show()
    while True:
        keypad.poll()
        for key in keypad.pressed():
            for entry in menu:
                if entry[0] == key:
                    return entry[2]

text = ""

PICTURE_MENU = [
    ("1", "Foto aufnehmen", "take"),
    ("0", "Abbrechen", "abort")
]

def take_picture():
    choice = show_menu(PICTURE_MENU)
    if choice == "take":
        image = camera.save_picture("splash")
        display.show_raw(camera.load_picture("splash"))
        time.sleep(5)
    return "main_menu"


MAIN_MENU = [
    ("1", "Kasse", "register"),
    ("2", "Foto", "take_picture"),
    ("0", "Abschalten", "quit")
]

def main_menu():
    return show_menu(MAIN_MENU)

FUNCTIONS = locals()

def main():
    mode = "main_menu"
    while mode != "quit":
        result = FUNCTIONS.get(mode)()
        if result:
            mode = result
    display.show_raw(camera.load_picture("splash"))
    power_off()

if __name__ == '__main__':
    main()
