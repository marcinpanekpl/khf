import ImageTk

__author__ = 'marc'


class TKRenderer:

    def renderPhoto(self, photo):
        return ImageTk.PhotoImage(photo)

    def showBinaryBitmap(self, bitmap):
        return ImageTk.BitmapImage(bitmap)