import display
import time

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def main():
    d = display.Display()
    d.clear()
    time.sleep(2)
    d.text(10, 10, "Hallo Jules")
    d.show(fast=True)


if __name__ == '__main__':
    main()
