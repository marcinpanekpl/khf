import Image

__author__ = 'marc'

BITMAP_MODE = "1"
GREY_SCALE_MODE = "L"

class ImageHandler:

    def loadWelcomeImage(self):
        return Image.open("../GAIT/Depth0/0019.png")

    def loadGreyScaleImage(self, fileHandler):
        return Image.open(fileHandler).convert("L")

    def createNewBinaryBitmap(self, size, data):
        image = Image.new(BITMAP_MODE, size)
        image.putdata(data)
        return image


#from PIL import Image
#
#image = Image.open("/dane/work/rosm/GAIT/Depth0/0019.png", "r").convert("L")
#image2 = Image.open("/dane/work/rosm/GAIT/Depth0/0020.png", "r").convert("L")
#
#treshold = 200
#processor = GreyBitmapProcessor()
#outputImage = processor.createBinaryMotionMap(image, image2, treshold)
#
#
#def onlyPositives(x):
#    if (x > 0):
#        return x
#
##print map(onlyPositives, outputImage.getdata())
#print image.getpixel((1,2))
#print image2.getpixel((1,2))
#print outputImage.getpixel((1,2))
#
#print image.getpixel((20,0))
#print image2.getpixel((20,0))
#print outputImage.getpixel((20,0))
