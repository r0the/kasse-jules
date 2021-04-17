import epd4in2 as EPD
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont

DEFAULT_FONT = "/usr/share/fonts/truetype/piboto/Piboto-Regular.ttf"

EPD.init()
_dim = (EPD.width, EPD.height)
_image = PIL.Image.new('1', _dim, 1)
_draw = PIL.ImageDraw.Draw(_image)
_font = PIL.ImageFont.truetype(DEFAULT_FONT, 36)

def clear():
    _draw.rectangle([0, 0, EPD.width - 1, EPD.height - 1], fill=1)

def text(x, y, text):
    _draw.text((x, y), text, font=_font, fill=0)

def rectangle(x, y, w, h):
    _draw.rectangle([x, y, x + w - 1, y + h - 1], outline=0)
        
def show(fast=False):
    EPD.show_image(_image, fast=fast)

def show_raw(image):
    image = image.resize(_dim)
    EPD.show_image(image)
