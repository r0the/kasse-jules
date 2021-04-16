import epd4in2
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

DEFAULT_FONT = "/usr/share/fonts/truetype/piboto/Piboto-Regular.ttf"

class Display:
    def __init__(self):
        self.epd = epd4in2.EPD()
        self.image = Image.new('1', (self.epd.width, self.epd.height), 1)
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.truetype(DEFAULT_FONT, 36)

    def clear(self):
        self.epd.clear()

    def text(self, x, y, text):
        self.draw.text((x, y), text, font=self.font, fill=0)

    def show(self, fast=False):
        self.epd.show(self.image, fast=fast)
