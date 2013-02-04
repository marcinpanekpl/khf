import functools
import operator
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

    def createGreyBitmapWithDirectionInfo(self, image1, image2, THRESHOLD):
        self.assertCorrectInput(image1, image2, THRESHOLD)
        data = map(functools.partial(processPixelWithDirectionInfo, THRESHOLD=THRESHOLD), list(image1.getdata()), list(image2.getdata()))
        return ImageHandler().createNewGreyScaleBitmap(image1.size, data)

    def calculateMassCenterAndMotionVector(self, greyBitmapWithDirectionInfo, box):
        image = ImageHandler().createEmptyGreyScaleBitmap(greyBitmapWithDirectionInfo.size)
        image.paste(greyBitmapWithDirectionInfo.crop(box), box)
        first = self._calculateMassCenter(image, 1)
        second = self._calculateMassCenter(image, 2)
        return first, second


    def _calculateMassCenter(self, image, value):
        bitmap = image.load()
        points = 0
        coordinatesSum = (0,0)

        for i in xrange(image.size[0]):
            for j in xrange(image.size[1]):
                if bitmap[i,j] == value:
                    points += 1
                    coordinatesSum = map(operator.add, coordinatesSum, (i,j))

        return map(lambda x: x/points, coordinatesSum)


def processPixel(x, y, THRESHOLD):
    if abs(y - x) > THRESHOLD:
        return 1
    return 0

def processPixelWithDirectionInfo(x, y, THRESHOLD):
    if (y - x) > THRESHOLD:
        return 2
    elif (x - y) > THRESHOLD:
        return 1;
    return 0