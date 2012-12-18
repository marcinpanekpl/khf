__author__ = 'marc'
from ImageHandler import BITMAP_MODE

class BinaryBitmapProcessor:

    # zwracaj krotke z centrum masy
    def transformBitmapToReduceNoise(self, bitmap):
        assert bitmap.mode == BITMAP_MODE
        transformed = self.transformImageBitmapToDictionaryBitmap(bitmap)

        return

    def _transformImageBitmapToDictionaryBitmap(self, bitmap):

        return

    def __calculateCenterOfMass(self, bitmap):
        listData = bitmap.getdata()
        dimensions = bitmap.size
        for i in dimensions[0]:
            for j in dimensions[1]:
                return
                #if listData

        return

    def __calculateFarestPoint(self, bitmap, center):
        return
