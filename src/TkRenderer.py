import ImageTk

__author__ = 'marc'


class TKRenderer:

    def toPhotoImage(self, photo):
        return ImageTk.PhotoImage(photo)

    def toBinaryImage(self, bitmap):
        return ImageTk.BitmapImage(bitmap)