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
MENU_AMOUNT_X = 340

ITEMS = [
    [
        ("1", "Fondue", 12),
        ("2", "Riesen-Cervelas", 19),
        ("3", "Petit Beurre", 10),
        ("4", "Erdbeerkonfi", 9)
    ],[
        ("1", "Bio-Eier", 13),
        ("2", "Bio-Spiegelei", 5),
        ("3", "Piro-Erdbeere", 4),
        ("4", "My Proto Aromat", 3)
    ],[
        ("1", "Bananen-Teil", 1),
        ("2", "Krustenkranz", 11),
        ("3", "Le Gruyere", 1),
        ("4", "Slviro-Tomate", 1)
    ],[
        ("1", "Super-Seife", 20),
        ("2", "Slviro-Birne", 3),
        ("3", "Orangen-Apfel", 7),
        ("4", "Apfel-Orange", 7)
    ],[
        ("1", "Gelbe Aepfel", 5),
        ("2", "Zitronen-Kuala", 3),
        ("3", "Orangen-Kiwi", 10),
        ("4", "Schoggikuchen", 19)
    ]
]

basket_items = []

def power_off():
    subprocess.call("sudo shutdown --poweroff now", shell=True)

def show_items(items):
    display.clear()
    y = 0
    for item in items:
        display.text(MENU_KEY_X, y, item[0])
        display.text(MENU_TEXT_X, y, item[1])
        display.text(MENU_AMOUNT_X, y, str(item[2]))
        y = y + 50
    display.text(MENU_KEY_X, y, "*")
    display.text(MENU_TEXT_X, y, "mehr...")
    y = y + 50
    display.text(MENU_KEY_X, y, "#")
    display.text(MENU_TEXT_X, y, "Abbrechen")
    display.show()

def select_item():
    page = 0
    while True:
        show_items(ITEMS[page])
        while True:
            keypad.poll()
            for key in keypad.pressed():
                for item in ITEMS[page]:
                    if item[0] == key:
                        basket_items.append(item)
                        return "main_menu"
                if key == "#":
                    return "main_menu"
                if key == "*":
                    page = (page + 1) % len(ITEMS)
                    show_items(ITEMS[page])

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

def basket():
    if not len(basket_items):
        select_item()
    show_items(basket_items, "Warenkorb")
    while True:
        keypad.poll()
        for key in keypad.pressed():
            return "main_menu"


MAIN_MENU = [
    ("1", "Kasse", "basket"),
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
