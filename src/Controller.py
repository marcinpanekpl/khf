#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 16-12-2012

@author: Marcin Panek
'''
from PIL import ImageTk
from CacheHolder import CacheHolder
from GreyBitmapProcessor import GreyBitmapProcessor
from ImageHandler import ImageHandler

class Controller(object):
    '''
    classdocs
    '''
    current = -1
    cache = CacheHolder()
    imageLoader = ImageHandler()
    greyBitmapProcessor = GreyBitmapProcessor()

    def __init__(self, interface):
        '''
        Constructor
        '''
        # TODO: do dalszego refaktoringu: kontroler nie wie może wiedzieć o polach widoku
        self.inteface = interface

    def getImage(self):
        # TODO: najlepiej jakby nie wiedział o ImageTk - ale to trudne do zrealizowania jeżeli mamy generyczny generate
        return ImageTk.PhotoImage(self.imageLoader.loadWelcomeImage())

    def loadImage(self, fileHandler):
        imgFile = self.imageLoader.loadGreyScaleImage(fileHandler)
        self.current = self.cache.store(imgFile)
        return ImageTk.PhotoImage(imgFile)

    def goBack(self):
        if (self.current > 0):
            self.current -= 1
            return ImageTk.PhotoImage(self.cache.get(self.current))
    
    def goNext(self):
        if (self.current < self.cache.getTotal() ):
            self.current += 1
            return ImageTk.PhotoImage(self.cache.get(self.current))

    # TODO: jeżeli chcemy mieć generyczną metodę 'generate' dla wszystkich akcji to musimy brać jakąś mapę z wartościami
    # pól widoku
    def generate(self):
        """ Generate button handler"""
        
        # checkbox values
#        print self.inteface.binaryEnable.get()
#        print self.inteface.cogEnable.get()
#        print self.inteface.snakeEnable.get()
#
#        # parameters values
#        print self.inteface.binaryThreshold.get()
#
#        print self.inteface.cogValue.get()
#        print self.inteface.cogValue2.get()
#
#        print self.inteface.snakeValue.get()
#        print self.inteface.snakeValue2.get()
#        print self.inteface.snakeValue3.get()

        img = None
        if (self.inteface.binaryEnable.get() == 1 and (self.cache.get(self.current)) != None):
            img = self.greyBitmapProcessor.createBinaryMotionMap((self.cache.get(self.current - 1)),
                self.cache.get(self.current), int(self.inteface.binaryThreshold.get()))

        if (img != None):
            return ImageTk.BitmapImage(img)

        return None
