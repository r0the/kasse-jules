import display


from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def main():
    d = display.Display()
    d.text(10, 10, "Hallo Jules")
    d.show()


if __name__ == '__main__':
    main()
