import functools
from ImageHandler import GREY_SCALE_MODE, ImageHandler

__author__ = 'marc'

class GreyBitmapProcessor:

    def assertCorrectInput(self, image1, image2, TRESHOLD):
        assert image1.size == image2.size
        assert image1.mode == GREY_SCALE_MODE
        assert image2.mode == GREY_SCALE_MODE
        assert TRESHOLD <= 255 and TRESHOLD >= 0

    def createBinaryMotionMap(self, image1, image2, TRESHOLD):
        self.assertCorrectInput(image1, image2, TRESHOLD)
        data = map(functools.partial(processPixel, TRESHOLD=TRESHOLD), list(image1.getdata()), list(image2.getdata()))
        return ImageHandler().createNewBinaryBitmap(image1.size, data)


def processPixel(x, y, TRESHOLD):
    if abs(y - x) > TRESHOLD:
        return 1
    return 0