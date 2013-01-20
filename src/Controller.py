#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 16-12-2012

@author: Marcin Panek
'''
import Image
import ImageDraw
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
        return self.renderer.toPhotoImage(imgFile)

    def addImage(self, image):
        self.current = self.cache.store(image)

    def goBack(self):
        if self.current > 0:
            self.current -= 1
            return self.renderer.toPhotoImage(self.cache.get(self.current))
    
    def goNext(self):
        if self.current < self.cache.getTotal():
            self.current += 1
            return self.renderer.toPhotoImage(self.cache.get(self.current))

    def clearCache(self):
        self.cache.clear()
        self.current = -1

    ### Algorithm parts

    def generateBinaryMotionBitmap(self, threshold):
        img = self.greyBitmapProcessor.createBinaryMotionMap((self.cache.get(0)),
            self.cache.get(1), threshold)
        self.addImage(img.convert("L"))

        return img.convert("1")

    def generatePreprocessedBitmap(self, img, erosionLoops, densityCoefficient):
        preprocessedImg = self.binaryBitmapProcessor.preprocess(img, erosionLoops, densityCoefficient)
        self.addImage(preprocessedImg.convert("L"))

        return preprocessedImg.convert("1")

    def generateBitmapWithMassCenter(self, img, distanceFromCenterCoefficient):
        (center, box, calculatedImg) = self.binaryBitmapProcessor.calculateMassCenter(img,
            distanceFromCenterCoefficient)
        photo = self.imageHandler.createNewRGBFromBinaryBitmap(img)
        self.imageHandler.putRedBoxIntoPicture(photo, box)
        self.imageHandler.putBigRedPoint(photo, center)
        self.addImage(photo)

        return photo, center, box

    def releaseTheSnake(self, img, center, box, snakeValue, snakeValue1, snakeValue2):
        return img

    ###

    ### Buttons handlers

    def getBinaryMotionBitmap(self, threshold):
        if self.cache.getTotal() + 1 >= 2:
            img = self.generateBinaryMotionBitmap(threshold)
            return self.renderer.toPhotoImage(img.convert("L"))
        else:
            # TODO error dialog
            print "Not enough images loaded"

    def getPreprocessedBitmap(self, threshold, erosionLoops, densityCoefficient):
        if self.cache.get(0) is not None and self.cache.get(1) is not None:
            img = self.generateBinaryMotionBitmap(threshold)
            img = self.generatePreprocessedBitmap(img, erosionLoops, densityCoefficient)
            return self.renderer.toPhotoImage(img.convert("L"))

    def getBitmapWithMassCenter(self, threshold, erosionLoops, densityCoefficient, distanceFromCenterCoefficient):
        if self.cache.get(0) is not None and self.cache.get(1) is not None:
            img = self.generateBinaryMotionBitmap(threshold)
            img = self.generatePreprocessedBitmap(img, erosionLoops, densityCoefficient)
            img, center, box = self.generateBitmapWithMassCenter(img, distanceFromCenterCoefficient)
            return self.renderer.toPhotoImage(img)

    def getTheSnake(self, threshold, erosionLoops, densityCoefficient, distanceFromCenterCoefficient, snakeValue, snakeValue1, snakeValue2):
        if self.cache.get(0) is not None and self.cache.get(1) is not None:
#            img = self.generateBinaryMotionBitmap(threshold)
#            img = self.generatePreprocessedBitmap(img, erosionLoops, densityCoefficient)
#            imgWithBox, center, box = self.generateBitmapWithMassCenter(img, distanceFromCenterCoefficient)
#            newBox = (box(0), box(1), box(2), box(3))
            img = Image.open("image1.bmp").convert("RGB")
            photo = img.copy()
            center = (187, 232)
            box = (11,73,403,390) # original values
            box = (100,70,300,400)
            draw = ImageDraw.Draw(photo)
            draw.rectangle(box, outline="red")
            self.imageHandler.putBigRedPoint(photo, center)
            photo.show()

            imgWithSnake = self.releaseTheSnake(img.convert("1"), center, box, snakeValue, snakeValue1, snakeValue2)
            return self.renderer.toPhotoImage(img)
    ###