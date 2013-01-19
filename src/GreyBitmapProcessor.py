import functools
from ImageHandler import GREY_SCALE_MODE, ImageHandler

__author__ = 'marc'

class GreyBitmapProcessor:

    def assertCorrectInput(self, image1, image2, THRESHOLD):
        assert image1.size == image2.size
        assert image1.mode == GREY_SCALE_MODE
        assert image2.mode == GREY_SCALE_MODE
        assert 255 >= THRESHOLD >= 0

    def createBinaryMotionMap(self, image1, image2, THRESHOLD):
        self.assertCorrectInput(image1, image2, THRESHOLD)
        data = map(functools.partial(processPixel, THRESHOLD=THRESHOLD), list(image1.getdata()), list(image2.getdata()))
        return ImageHandler().createNewBinaryBitmap(image1.size, data)


def processPixel(x, y, THRESHOLD):
    if abs(y - x) > THRESHOLD:
        return 1
    return 0