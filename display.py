import epd4in2 as EPD
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

DEFAULT_FONT = "/usr/share/fonts/truetype/piboto/Piboto-Regular.ttf"

EPD.init()
_image = Image.new('1', (EPD.width, EPD.height), 1)
_draw = ImageDraw.Draw(_image)
_font = ImageFont.truetype(DEFAULT_FONT, 36)

def clear():
    EPD.clear()

def text(x, y, text):
    _draw.text((x, y), text, font=_font, fill=0)

def show(fast=False):
    EPD.show_image(_image, fast=fast)
