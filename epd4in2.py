##
 #  @filename   :   epd4in2.py
 #  @brief      :   Implements for e-paper library
 #  @authors    :   Yehui from Waveshare, Stefan Rothe
 #
 #  Copyright (C) Waveshare     September 9 2017
 #  Copyright (C) Stefan Rothe  2021
 #
 # Permission is hereby granted, free of charge, to any person obtaining a copy
 # of this software and associated documnetation files (the "Software"), to deal
 # in the Software without restriction, including without limitation the rights
 # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 # copies of the Software, and to permit persons to  whom the Software is
 # furished to do so, subject to the following conditions:
 #
 # The above copyright notice and this permission notice shall be included in
 # all copies or substantial portions of the Software.
 #
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 # FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 # LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 # THE SOFTWARE.
 #

import RPi.GPIO as GPIO
import spidev
import time

BUSY_PIN = 24
CS_PIN = 8
DC_PIN = 25
RESET_PIN = 17

# GDEW042T2 commands
PANEL_SETTING                               = 0x00
POWER_SETTING                               = 0x01
POWER_OFF                                   = 0x02
POWER_OFF_SEQUENCE_SETTING                  = 0x03
POWER_ON                                    = 0x04
POWER_ON_MEASURE                            = 0x05
BOOSTER_SOFT_START                          = 0x06
DEEP_SLEEP                                  = 0x07
DATA_START_TRANSMISSION_1                   = 0x10
DATA_STOP                                   = 0x11
DISPLAY_REFRESH                             = 0x12
DATA_START_TRANSMISSION_2                   = 0x13
LUT_FOR_VCOM                                = 0x20 
LUT_WHITE_TO_WHITE                          = 0x21
LUT_BLACK_TO_WHITE                          = 0x22
LUT_WHITE_TO_BLACK                          = 0x23
LUT_BLACK_TO_BLACK                          = 0x24
PLL_CONTROL                                 = 0x30
VCOM_AND_DATA_INTERVAL_SETTING              = 0x50
TCON_SETTING                                = 0x60
RESOLUTION_SETTING                          = 0x61
GSST_SETTING                                = 0x65
GET_STATUS                                  = 0x71
AUTO_MEASUREMENT_VCOM                       = 0x80
VCM_DC_SETTING                              = 0x82
PARTIAL_WINDOW                              = 0x90
PARTIAL_IN                                  = 0x91
PARTIAL_OUT                                 = 0x92

REFRESH_DEFAULT = [
    [ # vcom
        0x00, 0x17, 0x00, 0x00, 0x00, 0x02,      
        0x00, 0x17, 0x17, 0x00, 0x00, 0x02,      
        0x00, 0x0A, 0x01, 0x00, 0x00, 0x01,      
        0x00, 0x0E, 0x0E, 0x00, 0x00, 0x02,      
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,      
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,      
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00,
    ],
    [ # ww
        0x40, 0x17, 0x00, 0x00, 0x00, 0x02,
        0x90, 0x17, 0x17, 0x00, 0x00, 0x02,
        0x40, 0x0A, 0x01, 0x00, 0x00, 0x01,
        0xA0, 0x0E, 0x0E, 0x00, 0x00, 0x02,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ],
    [ # bw
        0x40, 0x17, 0x00, 0x00, 0x00, 0x02,
        0x90, 0x17, 0x17, 0x00, 0x00, 0x02,
        0x40, 0x0A, 0x01, 0x00, 0x00, 0x01,
        0xA0, 0x0E, 0x0E, 0x00, 0x00, 0x02,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ],
    [ # bb
        0x80, 0x17, 0x00, 0x00, 0x00, 0x02,
        0x90, 0x17, 0x17, 0x00, 0x00, 0x02,
        0x80, 0x0A, 0x01, 0x00, 0x00, 0x01,
        0x50, 0x0E, 0x0E, 0x00, 0x00, 0x02,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ],
    [ # wb
        0x80, 0x17, 0x00, 0x00, 0x00, 0x02,
        0x90, 0x17, 0x17, 0x00, 0x00, 0x02,
        0x80, 0x0A, 0x01, 0x00, 0x00, 0x01,
        0x50, 0x0E, 0x0E, 0x00, 0x00, 0x02,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
]

REFRESH_FAST = [
    [ # vcom
        0x00, 0x19, 0x01, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00
    ],
    [ # ww
        0x00, 0x19, 0x01, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ],
    [ # ww
        0x80, 0x19, 0x01, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ],
    [ # wb
        0x40, 0x19, 0x01, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ],
    [ # bb
        0x00, 0x19, 0x01, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
]

# initialise serial peripheral interface
_spi = spidev.SpiDev(0, 0)
_spi.max_speed_hz = 2000000
_spi.mode = 0b00

# initialise additional pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(BUSY_PIN, GPIO.IN)
GPIO.setup(CS_PIN, GPIO.OUT)
GPIO.setup(DC_PIN, GPIO.OUT)
GPIO.setup(RESET_PIN, GPIO.OUT)

# initialise screen size and buffer
width = 400
height = 300
_buffer = [0] * (width * height // 8)

def _send_command(command):
    GPIO.output(DC_PIN, GPIO.LOW)
    _spi.writebytes([command])

def _send_data(data):
    GPIO.output(DC_PIN, GPIO.HIGH)
    _spi.writebytes([data])

def _sleep_ms(milliseconds):
    time.sleep(milliseconds // 1000)

def _wait_until_idle():
    while GPIO.input(BUSY_PIN) == 0:
        _sleep_ms(100)

def _set_lut(lut):
    for i in range(len(lut)):
        _send_command(LUT_FOR_VCOM + i)
        table = lut[i]
        for j in range(len(table)):
            _send_data(table[j])

def _display_buffer(fast=False):
    if fast:
        _set_lut(REFRESH_FAST)
    else:
        _set_lut(REFRESH_DEFAULT)
    _send_command(DATA_START_TRANSMISSION_1)
    for i in range(len(_buffer)):
        _send_data(0xFF)       # bit set: white, bit reset: black
    _sleep_ms(2)
    _send_command(DATA_START_TRANSMISSION_2) 
    for i in range(len(_buffer)):
        _send_data(_buffer[i])
    _sleep_ms(2)
    _send_command(DISPLAY_REFRESH)
    if not fast:
        _sleep_ms(100)
        _wait_until_idle()

def reset():
    GPIO.output(RESET_PIN, GPIO.LOW)
    _sleep_ms(200)
    GPIO.output(RESET_PIN, GPIO.HIGH)
    _sleep_ms(200)

def init():
    reset()
    _send_command(POWER_SETTING)
    _send_data(0x03)                  # VDS_EN, VDG_EN
    _send_data(0x00)                  # VCOM_HV, VGHL_LV[1], VGHL_LV[0]
    _send_data(0x2b)                  # VDH
    _send_data(0x2b)                  # VDL
    _send_data(0xff)                  # VDHR
    _send_command(BOOSTER_SOFT_START)
    _send_data(0x17)
    _send_data(0x17)
    _send_data(0x17)                  #07 0f 17 1f 27 2F 37 2f
    _send_command(POWER_ON)
    _wait_until_idle()
    _send_command(PANEL_SETTING)
    _send_data(0xbf) # KW-BF   KWR-AF  BWROTP 0f
    _send_data(0x0b)
    _send_command(PLL_CONTROL)
    _send_data(0x3c) # 3A 100HZ   29 150Hz 39 200HZ  31 171HZ
    _send_command(RESOLUTION_SETTING)
    _send_data(width >> 8)        
    _send_data(width & 0xff)
    _send_data(height >> 8)
    _send_data(height & 0xff)
    _send_command(VCM_DC_SETTING)
    _send_data(0x12)                   
    _send_command(VCOM_AND_DATA_INTERVAL_SETTING)
    _send_command(0x97)    #VBDF 17|D7 VBDW 97  VBDB 57  VBDF F7  VBDW 77  VBDB 37  VBDR B7

def clear():
    for i in range(len(_buffer)):
        _buffer[i] = 0xFF
    _display_buffer()
        
def show_image(image, fast=False):
    # Set buffer to value of Python Imaging Library image.
    # Image must be in mode 1.
    image_monocolor = image.convert('1')
    w, h = image_monocolor.size
    if w != width or h != height:
        raise ValueError('Image must be same dimensions as display ({0}x{1}).' .format(width, height))
    pixels = image_monocolor.load()
    bit = 0x80
    byte = 0
    for y in range(height):
        for x in range(width):
            if pixels[x, y]:
                _buffer[byte] |= bit
            else:
                _buffer[byte] &= ~bit
            if bit == 0x01:
                bit = 0x80
                byte += 1
            else:
                bit >>= 1
    _display_buffer(fast=fast)
