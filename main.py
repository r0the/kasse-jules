import display
import time

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def main():
    display.clear()
    display.text(10, 10, "Kasse von Jules")
    display.text(10, 60, "Version 0.1")
    display.show(fast=True)


if __name__ == '__main__':
    main()
