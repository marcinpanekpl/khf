from __future__ import division
import functools
import math
import operator

__author__ = 'marc'
from ImageHandler import BITMAP_MODE, ImageHandler


def createHorizontalListOfCoordinates(list, value):
    return map(functools.partial(lambda x,y: (x,y), y=value), list)

def createVerticalListOfCoordinates(list, value):
    return map(functools.partial(lambda x,y: (y,x), y=value), list)

class BinaryBitmapVerticalTransformer:

    def preprocessBitmapVertically(self, bitmap, densityCoefficient):
        sums = []
        for x in xrange(bitmap.size[0]):
            sum = 0
            for y in xrange(bitmap.size[1]):
                sum += bitmap.getpixel((x,y))
            sums += [sum]

        maxDensity = max(sums)
        for x in xrange(bitmap.size[0]):
            if (sums[x] < densityCoefficient*maxDensity/100):
                bitmap.paste(0, (x, 0, x+1, bitmap.size[1]))

class BinaryBitmapNoiseTransformer:

    def reduceNoise(self, bitmap, distanceFromCenterCoefficient):
        (coordinatesSum, points) = self._calculateCoordinatesSum(bitmap)
        noise = True
        while(noise and points > 0):
            center = map(lambda x: x/points, coordinatesSum)
            farest = self._calculateFarestPointFromTheBox(bitmap, center)
            noise = self._decideWhetherRemovePixel(center, farest, bitmap.size[1]*(1-distanceFromCenterCoefficient/100))
            if (noise):
                bitmap.paste(0, farest + tuple(map(operator.add, farest, (1,1))))
                points -= 1
                coordinatesSum = map(operator.sub, coordinatesSum, farest)

        return (tuple(map(lambda x: int(x), center)), bitmap.getbbox())

    def _calculateCoordinatesSum(self, bitmap):
        points = 0
        coordinatesSum = (0,0)

        for i in xrange(bitmap.size[0]):
            for j in xrange(bitmap.size[1]):
                if (bitmap.getpixel((i,j)) > 0):
                    points += 1
                    coordinatesSum = map(operator.add, coordinatesSum, (i,j))

        return (coordinatesSum, points)

    def _calculateFarestPointFromTheBox(self, bitmap, center):
        maxDistance = 0
        farest = (0,0)
        (left, upper, right, lower) = bitmap.getbbox()
        horizontal = xrange(left, right)
        vertical = xrange(upper, lower)
        coordinatesList = createVerticalListOfCoordinates(vertical, left) +\
                          createVerticalListOfCoordinates(vertical, right-1) +\
                          createHorizontalListOfCoordinates(horizontal, upper) +\
                          createHorizontalListOfCoordinates(horizontal, lower-1)

        #print coordinatesList.__len__()
        #print coordinatesList
        for xy in coordinatesList:
            key = bitmap.getpixel(xy)
            if (key > 0):
                distance = self._calculateDistance(xy, center)
                if (distance > maxDistance):
                    maxDistance = distance
                    farest = xy

        #print "f, c, dist: " + farest.__str__(), center.__str__(), distance.__str__()
        return farest

    def _decideWhetherRemovePixel(self, center, farest, maxDistanceFromCenter):
        return True if (self._calculateDistance(center, farest) > maxDistanceFromCenter) else False

    def _calculateDistance(self, pixel1, pixel2):
        return math.sqrt(pow(pixel1[0]-pixel2[0], 2) + pow(pixel1[1]-pixel2[1], 2))


class BinaryBitmapProcessor:

    # zwracaj krotke z trzema elementami:
    # 1: krotka centrum masy x,y
    # 2: krotka wspolrzedne prostoka left, upper, right, lower
    # 3: przesztalcona bitmapa
    verticalPreprocessor = BinaryBitmapVerticalTransformer()
    bitmapProcessor = BinaryBitmapNoiseTransformer()

    def reduceNoiseAndCalculateMassCenter(self, bitmap, densityCoefficient, distanceFromCenterCoefficient):
        assert bitmap.mode == BITMAP_MODE
        transformed = bitmap.copy()
        self.verticalPreprocessor.preprocessBitmapVertically(transformed, densityCoefficient)
        (center, box) = self.bitmapProcessor.reduceNoise(transformed, distanceFromCenterCoefficient)
        print center, box
        return (center, box, ImageHandler().createNewBinaryBitmap(transformed.size, transformed.getdata()))