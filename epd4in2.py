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

from PIL import Image
from epdif import EPDIf
import time
import spidev
import RPi.GPIO as GPIO

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

class EPD(EPDIf):
    def __init__(self, **kvargs):
        EPDIf.__init__(self, **kvargs)
        self.width = 400
        self.height = 300
        self.buffer = [0] * (self.width * self.height // 8)
        self.lut = REFRESH_DEFAULT

    def init(self):
        self.reset()
        self.send_command(POWER_SETTING)
        self.send_data(0x03)                  # VDS_EN, VDG_EN
        self.send_data(0x00)                  # VCOM_HV, VGHL_LV[1], VGHL_LV[0]
        self.send_data(0x2b)                  # VDH
        self.send_data(0x2b)                  # VDL
        self.send_data(0xff)                  # VDHR
        self.send_command(BOOSTER_SOFT_START)
        self.send_data(0x17)
        self.send_data(0x17)
        self.send_data(0x17)                  #07 0f 17 1f 27 2F 37 2f
        self.send_command(POWER_ON)
        self.wait_until_idle()
        self.send_command(PANEL_SETTING)
        self.send_data(0xbf) # KW-BF   KWR-AF  BWROTP 0f
        self.send_data(0x0b)
        self.send_command(PLL_CONTROL)
        self.send_data(0x3c) # 3A 100HZ   29 150Hz 39 200HZ  31 171HZ
        self.send_command(RESOLUTION_SETTING)
        self.send_data(self.width >> 8)        
        self.send_data(self.width & 0xff)
        self.send_data(self.height >> 8)
        self.send_data(self.height & 0xff)
        self.send_command(VCM_DC_SETTING)
        self.send_data(0x12)                   
        self.send_command(VCOM_AND_DATA_INTERVAL_SETTING)
        self.send_command(0x97)    #VBDF 17|D7 VBDW 97  VBDB 57  VBDF F7  VBDW 77  VBDB 37  VBDR B7

    def clear(self):
        for i in range(len(self.buffer)):
            self.buffer[i] = 0xFF
        self.display_buffer()
        
    def set_lut(self, lut):
        for i in range(len(lut)):
            self.send_command(LUT_FOR_VCOM + i)
            table = lut[i]
            for j in range(len(table)):
                self.send_data(table[j])

    def show(self, image, fast=False):
        # Set buffer to value of Python Imaging Library image.
        # Image must be in mode 1.
        image_monocolor = image.convert('1')
        w, h = image_monocolor.size
        if w != self.width or h != self.height:
            raise ValueError('Image must be same dimensions as display ({0}x{1}).' .format(self.width, self.height))
        pixels = image_monocolor.load()
        bit = 0x80
        byte = 0
        for y in range(self.height):
            for x in range(self.width):
                if pixels[x, y]:
                    self.buffer[byte] |= bit
                else:
                    self.buffer[byte] &= ~bit
                if bit == 0x01:
                    bit = 0x80
                    byte += 1
                else:
                    bit >>= 1
        self.display_buffer(fast=fast)

    def display_buffer(self, fast=False):
        if fast:
            self.set_lut(REFRESH_FAST)
        else:
            self.set_lut(REFRESH_DEFAULT)
        self.send_command(DATA_START_TRANSMISSION_1)
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(0xFF)       # bit set: white, bit reset: black
        self.sleep_ms(2)
        self.send_command(DATA_START_TRANSMISSION_2) 
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(self.buffer[i])
        self.sleep_ms(2)
        self.send_command(DISPLAY_REFRESH)
        if not fast:
            self.sleep_ms(100)
            self.wait_until_idle()
