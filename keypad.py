import RPi.GPIO as GPIO

ROW_PINS = [12, 13, 14]
COL_PINS = [15, 16, 17, 18]
MATRIX = [
    ["1", "2", "3"],
    ["4", "5", "6"],
    ["7", "8", "9"],
    ["*", "0", "#"]
]

def _init():
    for pin in COL_PINS:
        GPIO.setup(pin, GPIO.OUT)
    for pin in ROW_PINS:
        GPIO.setup(pin, GPIO.IN)


def

_init()