import RPi.GPIO as GPIO

ROW_PINS = [27, 14, 15, 23]
COL_PINS = [17, 22, 18]
MATRIX = [
    ["1", "2", "3"],
    ["4", "5", "6"],
    ["7", "8", "9"],
    ["*", "0", "#"]
]

_pressed = []
_previous = []

for col_pin in COL_PINS:
    GPIO.setup(col_pin, GPIO.OUT, initial=GPIO.LOW)
for row_pin in ROW_PINS:
    GPIO.setup(row_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def poll():
    global _pressed
    global _previous
    _previous = _pressed
    _pressed = []
    for col in range(len(COL_PINS)):
        GPIO.output(COL_PINS[col], GPIO.HIGH)
        for row in range(len(ROW_PINS)):
            if GPIO.input(ROW_PINS[row]):
                key = MATRIX[row][col]
                _pressed.append(key)
        GPIO.output(COL_PINS[col], GPIO.LOW)

def pressed():
    result = []
    for key in _pressed:
        if not key in _previous:
            result.append(key)
    return result
