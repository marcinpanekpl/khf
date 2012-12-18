__author__ = 'marc'


class CacheHolder:

    images = []

    def store(self, imgFile):
        self.images.append(imgFile)
        return self.getTotal()

    def get(self, number):
        if (self.getTotal() >= 0):
            return self.images[number]
        return None

    def getTotal(self):
        return self.images.__len__() - 1