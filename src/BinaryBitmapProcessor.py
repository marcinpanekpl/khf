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

class BinaryBitmapPreprocessor:

    def preprocessBitmapVertically(self, bitmap, densityCoefficient):
        sums = []
        for x in xrange(bitmap.size[0]):
            sum = 0
            for y in xrange(bitmap.size[1]):
                sum += bitmap.getpixel((x,y)) # TODO ->[] version
            sums += [sum]

        maxDensity = max(sums)
        for x in xrange(bitmap.size[0]):
            if sums[x] < densityCoefficient*maxDensity/100:
                bitmap.paste(0, (x, 0, x+1, bitmap.size[1]))

    def erosion(self, image, erosionLoops):
        '''
        Classic erosion algorithm.
        Uses temporary '2' values to distinct values changed in this loop.
        '''
        bitmap = image.load()

        for i in range(erosionLoops):
            for x in range(image.size[0]):
                for y in range(image.size[1]):
                    if bitmap[x,y] == 1:
                        if  (x>0 and bitmap[x-1,y] == 0) or\
                            (y>0 and bitmap[x, y-1] == 0) or\
                            (x+1 < image.size[0] and bitmap[x+1, y] == 0) or\
                            (y+1 < image.size[1] and bitmap[x, y+1] == 0):
                                bitmap[x, y] = 2

            for x in range(image.size[0]):
                for y in range(image.size[1]):
                    if bitmap[x,y] == 2:
                        bitmap[x,y] = 0


class BinaryBitmapNoiseTransformer:

    def reduceNoise(self, bitmap, distanceFromCenterCoefficient):
        normalizedDistanceFromCenter = bitmap.size[1]*(1-distanceFromCenterCoefficient/100)
        (coordinatesSum, points) = self._calculateCoordinatesSum(bitmap)
        noise = True
        while noise and points > 0:
            center = map(lambda x: x/points, coordinatesSum)
            farest = self._calculateFarestPointFromTheBox(bitmap, center)
            noise = self._decideWhetherRemovePixel(center, farest, normalizedDistanceFromCenter)
            if noise:
                bitmap.paste(0, farest + tuple(map(operator.add, farest, (1,1))))
                points -= 1
                coordinatesSum = map(operator.sub, coordinatesSum, farest)

        return tuple(map(lambda x: int(x), center)), bitmap.getbbox()

    def _calculateCoordinatesSum(self, image):
        bitmap = image.load()
        points = 0
        coordinatesSum = (0,0)

        for i in xrange(image.size[0]):
            for j in xrange(image.size[1]):
                if bitmap[i,j] > 0:
                    points += 1
                    coordinatesSum = map(operator.add, coordinatesSum, (i,j))

        return coordinatesSum, points

    def _calculateFarestPointFromTheBox(self, image, center):
        bitmap = image.load()
        maxDistance = 0
        furthest = (0,0)
        (left, upper, right, lower) = image.getbbox()
        horizontal = xrange(left, right)
        vertical = xrange(upper, lower)
        coordinatesList = createVerticalListOfCoordinates(vertical, left) +\
                          createVerticalListOfCoordinates(vertical, right-1) +\
                          createHorizontalListOfCoordinates(horizontal, upper) +\
                          createHorizontalListOfCoordinates(horizontal, lower-1)

        #print coordinatesList.__len__()
        #print coordinatesList
        for xy in coordinatesList:
            key = bitmap[xy[0],xy[1]]
            if key > 0:
                distance = self._calculateDistance(xy, center)
                if distance > maxDistance:
                    maxDistance = distance
                    furthest = xy

        #print "f, c, dist: " + furthest.__str__(), center.__str__(), distance.__str__()
        return furthest

    def _decideWhetherRemovePixel(self, center, farest, maxDistanceFromCenter):
        return True if (self._calculateDistance(center, farest) > maxDistanceFromCenter) else False

    def _calculateDistance(self, pixel1, pixel2):
        return math.sqrt(pow(pixel1[0]-pixel2[0], 2) + pow(pixel1[1]-pixel2[1], 2))


class BinaryBitmapProcessor:

    # zwracaj krotke z trzema elementami:
    # 1: krotka centrum masy x,y
    # 2: krotka wspolrzedne prostoka left, upper, right, lower
    # 3: przeksztalcona bitmapa
    verticalPreprocessor = BinaryBitmapPreprocessor()
    bitmapProcessor = BinaryBitmapNoiseTransformer()

    def preprocess(self, bitmap, erosionLoops, densityCoefficient):
        transformed = bitmap.copy()
#        self.verticalPreprocessor.preprocessBitmapVertically(transformed, densityCoefficient)
        self.verticalPreprocessor.erosion(transformed, erosionLoops)
        return transformed

    def calculateMassCenter(self, bitmap, distanceFromCenterCoefficient):
        assert bitmap.mode == BITMAP_MODE
        transformed = bitmap.copy()
        (center, box) = self.bitmapProcessor.reduceNoise(transformed, distanceFromCenterCoefficient)
        return center, box, ImageHandler().createNewBinaryBitmap(transformed.size, transformed.getdata())