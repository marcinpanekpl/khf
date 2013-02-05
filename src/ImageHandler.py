from mimify import File
import Image
import operator
import os
import ImageDraw

__author__ = 'marc'

BITMAP_MODE = "1"
GREY_SCALE_MODE = "L"
RGB_MODE = "RGB"

COLOR_MAX_VALUE = 255
RED_COLOR = (COLOR_MAX_VALUE, 0, 0)

class ImageHandler:

    def loadGreyScaleImage(self, fileHandler):
        return Image.open(fileHandler).convert("L")

    def createNewBinaryBitmap(self, size, data):
        image = Image.new(BITMAP_MODE, size)
        image.putdata(data)
        return image

    def createNewRGBFromBinaryBitmap(self, bitmap):
        rgb = Image.new(RGB_MODE, bitmap.size)
        rgb.putdata(map(lambda x: (x*COLOR_MAX_VALUE, x*COLOR_MAX_VALUE, x*COLOR_MAX_VALUE), bitmap.getdata()))
        return rgb

    def putRedBoxIntoPicture(self, picture, boxCoordinates):
        (left, upper, right, lower) = boxCoordinates
        picture.paste(RED_COLOR, (left, upper, right, upper+1))
        picture.paste(RED_COLOR, (left, upper, left+1, lower))
        picture.paste(RED_COLOR, (right, upper, right+1, lower))
        picture.paste(RED_COLOR, (left, lower, right, lower+1))

    def putBigRedPoint(self, picture, point, size=3, color=RED_COLOR):
        picture.paste(color, tuple(map(operator.sub, point, (size, size))) + tuple(map(operator.add, point, (size, size))))