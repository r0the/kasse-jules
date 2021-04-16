##
 #  @filename   :   epdif.py
 #  @brief      :   EPD hardware interface implements (GPIO, SPI)
 #  @author     :   Yehui from Waveshare, Stefan Rothe
 #
 #  Copyright (C) Waveshare     July 10 2017
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

import spidev
import RPi.GPIO as GPIO
import time

class EPDIf:
    def __init__(self, busy_pin=24, cs_pin=8, dc_pin=25, reset_pin=17):
        self.busy_pin = busy_pin
        self.cs_pin = cs_pin
        self.dc_pin = dc_pin
        self.reset_pin = reset_pin
        self.spi = spidev.SpiDev(0, 0)
        self.spi.max_speed_hz = 2000000
        self.spi.mode = 0b00
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.busy_pin, GPIO.IN)
        GPIO.setup(self.cs_pin, GPIO.OUT)
        GPIO.setup(self.dc_pin, GPIO.OUT)
        GPIO.setup(self.reset_pin, GPIO.OUT)

    def reset(self):
        GPIO.output(self.reset_pin, GPIO.LOW)
        self.sleep_ms(200)
        GPIO.output(self.reset_pin, GPIO.HIGH)
        self.sleep_ms(200)

    def send_command(self, command):
        GPIO.output(self.dc_pin, GPIO.LOW)
        self.spi.writebytes([command])

    def send_data(self, data):
        GPIO.output(self.dc_pin, GPIO.HIGH)
        self.spi.writebytes([data])

    def sleep_ms(self, milliseconds):
        time.sleep(milliseconds // 1000)

    def wait_until_idle(self):
        while GPIO.input(self.busy_pin) == 0:
            self.sleep_ms(100)
