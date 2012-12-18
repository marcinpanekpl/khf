#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 16-12-2012

@author: Marcin Panek
'''
from PIL import ImageTk, Image

class Controller(object):
    '''
    classdocs
    '''
    images = []
    history= []

    def __init__(self, interface):
        '''
        Constructor
        '''
        self.inteface = interface
        
    def getImage(self):
        imgFile = Image.open("../img/0105.png")
        img = ImageTk.PhotoImage(imgFile)
        return img

    def goBack(self):
        pass
    
    def goNext(self):
        pass
    
    def generate(self):
        """ Generate button handler"""
        
        # checkbox values
        print self.inteface.binaryEnable.get()
        print self.inteface.cogEnable.get()
        print self.inteface.snakeEnable.get()
        
        # parameters values
        print self.inteface.binaryThreshold.get()
        
        print self.inteface.cogValue.get()
        print self.inteface.cogValue2.get()
        
        print self.inteface.snakeValue.get()
        print self.inteface.snakeValue2.get()
        print self.inteface.snakeValue3.get()
