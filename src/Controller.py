#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 16-12-2012

@author: Marcin Panek
'''
from BinaryBitmapProcessor import BinaryBitmapProcessor
from CacheHolder import CacheHolder
from GreyBitmapProcessor import GreyBitmapProcessor
from ImageHandler import ImageHandler

class Controller(object):
    '''
    classdocs
    '''
    current = -1
    cache = CacheHolder()
    greyBitmapProcessor = GreyBitmapProcessor()
    binaryBitmapProcessor = BinaryBitmapProcessor()
    imageHandler = ImageHandler()

    def __init__(self, renderer):
        '''
        Constructor
        '''
        self.renderer = renderer

    def loadImage(self, fileHandler):
        imgFile = self.imageHandler.loadGreyScaleImage(fileHandler)
        self.current = self.cache.store(imgFile)
        return self.renderer.renderPhoto(imgFile)

    def goBack(self):
        if self.current > 0:
            self.current -= 1
            return self.renderer.renderPhoto(self.cache.get(self.current))
    
    def goNext(self):
        if self.current < self.cache.getTotal():
            self.current += 1
            return self.renderer.renderPhoto(self.cache.get(self.current))

    def generateBinaryMotionBitmap(self, threshold):
        cacheSize = self.cache.getTotal() + 1
        self.current = cacheSize - 1

        if cacheSize >= 2:
            img = self.greyBitmapProcessor.createBinaryMotionMap((self.cache.get(self.current - 1)),
                     self.cache.get(self.current), threshold)
            return self.renderer.showBinaryBitmap(img)
        else:
            # TODO error dialog
            print "Not enough images loaded"
            return None


    def generateBitmapWithMassCenter(self, threshold, densityCoefficient, distanceFromCenterCoefficient):
        if self.cache.get(self.current) is not None:
            img = self.greyBitmapProcessor.createBinaryMotionMap(self.cache.get(self.current - 1),
                                                                 self.cache.get(self.current), threshold)
            (center, box, newImg) = self.binaryBitmapProcessor.reduceNoiseAndCalculateMassCenter(img,
                        densityCoefficient, distanceFromCenterCoefficient)
            photo = self.imageHandler.createNewRGBFromBinaryBitmap(img)
            self.imageHandler.putRedBoxIntoPicture(photo, box)
            self.imageHandler.putBigRedPoint(photo, center)
            return self.renderer.renderPhoto(photo)
