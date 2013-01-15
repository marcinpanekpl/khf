#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 16-12-2012

@author: Marcin Panek
'''

from Tkinter import Tk, Frame, Button, BOTH, LEFT, Label, N, E, S, W, \
    Checkbutton, BooleanVar, StringVar, Spinbox
from ttk import Style
from Controller import Controller
import sys
import tkFileDialog
from TkRenderer import TKRenderer


class Interface(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   

        self.parent = parent
        self.controller = Controller(TKRenderer())
        self.initUI()
    
    def initUI(self):
      
        self.parent.title("Kinect Human Finder")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)
        self.columnconfigure(1, weight=1, minsize=100, pad=10)
        self.rowconfigure(1, weight=1, minsize=100, pad=10)
        
        self.initHistoryFrame()
        self.initImageFrame()        
        self.initMenuFrame()
        
    def initHistoryFrame(self):    
        
        self.historyFrame = Frame(self, height=100, width=200, borderwidth=2)
        
        self.backButton = Button(self.historyFrame, text="Back", command=lambda: self.showImage(self.controller.goBack()))
        self.backButton.pack(side=LEFT, padx=5, pady=5)
        
        self.nextButton = Button(self.historyFrame, text="Next", command=lambda: self.showImage(self.controller.goNext()))
        self.nextButton.pack(side=LEFT, padx=5, pady=5)
        
        self.openButton = Button(self.historyFrame, text="Open", command=self.openFile)
        self.openButton.pack(side=LEFT, padx=(490,0), ipadx = 10, pady=5)

        self.historyFrame.grid(row=0, column=0, columnspan=2, sticky=W)
        
    def initImageFrame(self):
        
        self.imageFrame = Frame(self, borderwidth=2)
        self.showImage(self.controller.getImage())

        
    def initMenuFrame(self):
        
        self.menuFrame = Frame(self, width=400)
        self.menuFrame.grid(row=1, column=1, sticky=N + E + S + W)
        self.menuFrame.columnconfigure(0, weight=0, minsize=100, pad=10)

        # CheckBoxes
        binaryText = Label(self.menuFrame, text="Mapa binarna")
        cogText = Label(self.menuFrame, text="Środek ciężkości")
        snakeText = Label(self.menuFrame, text="Metoda aktywnych konturów")
        
        # Parameters
        self.binarySpinFrame = self.createBinarySpinBoxes()
        self.binarySpinFrame.grid(row=1, column=0, padx=36, pady=(5,15), stick=N + W)

        self.cogSpinFrame = self.createCogSpinBoxes()
        self.cogSpinFrame.grid(row=3, column=0, padx=36, pady=(0,15), stick=N + W)
        
        self.snakeSpinFrame = self.createSnakeSpinBoxes()
        self.snakeSpinFrame.grid(row=5, column=0, padx=36, pady=(0,15), stick=N + W)

        binaryText.grid(row=0, padx=15, stick=N + W)
        cogText.grid(row=2, padx=15, stick=N + W)
        snakeText.grid(row=4, padx=15, stick=N + W)
        
        # Generate
        self.generateButton = Button(self.menuFrame, text="Generuj mapą binarną",
            command=lambda: self.showImage(self.controller.generateBinaryMotionBitmap(
                int(self.binaryThreshold.get()))))
        self.generateButton.grid(row=6, column=0, padx=15, pady=(20,0), stick=N + W)

        self.generateButton = Button(self.menuFrame, text="Pokaż centrum masy",
            command=lambda: self.showImage(self.controller.generateBitmapWithMassCenter(
                int(self.binaryThreshold.get()), int(self.densityCoefficient.get()), int(self.distanceFromCenterCoefficient.get()))))
        self.generateButton.grid(row=7, column=0, padx=15, pady=(20,0), stick=N + W)

        self.generateButton = Button(self.menuFrame, text="Generate", command=lambda: self.showImage(self.controller.generate()))
        self.generateButton.grid(row=8, column=0, padx=15, pady=(20,0), stick=N + W)

    def createBinarySpinBoxes(self):
        frame = Frame(self.menuFrame, width=300)

        from_ = 0
        to = 255
        vcmd = (self.register(self.validateSpinBox),'%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        label1 = Label(frame, text="TRESHOLD (0,255)")
        self.binaryThreshold = StringVar(value="40")
        self.binarySpinBox = Spinbox(frame, textvariable=self.binaryThreshold, width=4, from_=from_, to=to, validate="key", validatecommand=vcmd) 
        
        label1.grid(row=0, column=0, padx=(0,10), stick=N+W)
        self.binarySpinBox.grid(row=0, column=1, stick=N+W)
        
        return frame
        
    def createCogSpinBoxes(self):
        frame = Frame(self.menuFrame, width=300)

        from_ = 0
        to = 100
        vcmd = (self.register(self.validateSpinBox),'%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        label1 = Label(frame, text="Wsp. kary za rzadkość")
        self.densityCoefficient = StringVar(value="50")
        self.cogSpinBox = Spinbox(frame, textvariable=self.densityCoefficient, width=4, from_=from_, to=to, validate="key", validatecommand=vcmd)
        
        label2 = Label(frame, text="Wsp. kary za odległość")
        self.distanceFromCenterCoefficient = StringVar(value="50")
        self.cogSpinBox2 = Spinbox(frame, textvariable=self.distanceFromCenterCoefficient, width=4, from_=from_, to=to, validate="key", validatecommand=vcmd)
        
        label1.grid(row=0, column=0, padx=(0,10), stick=N+W)
        label2.grid(row=1, column=0, padx=(0,10), stick=N+W)
        self.cogSpinBox.grid(row=0, column=1, stick=N+W)
        self.cogSpinBox2.grid(row=1, column=1, stick=N+W)
        
        return frame
        
    def createSnakeSpinBoxes(self):
        frame = Frame(self.menuFrame, width=300)

        from_ = 0
        to = 255
        vcmd = (self.register(self.validateSpinBox),'%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        label1 = Label(frame, text="Parametr 1")
        self.snakeValue = StringVar()
        self.snakeSpinBox = Spinbox(frame, textvariable=self.snakeValue, width=4, from_=from_, to=to, validate="key", validatecommand=vcmd) 
        
        label2 = Label(frame, text="Parametr 2")
        self.snakeValue2 = StringVar()
        self.snakeSpinBox2 = Spinbox(frame, textvariable=self.snakeValue2, width=4, from_=from_, to=to, validate="key", validatecommand=vcmd)
        
        label3 = Label(frame, text="Parametr 3")
        self.snakeValue3 = StringVar()
        self.snakeSpinBox3 = Spinbox(frame, textvariable=self.snakeValue3, width=4, from_=from_, to=to, validate="key", validatecommand=vcmd)
        
        label1.grid(row=0, column=0, padx=(0,10), stick=N+W)
        label2.grid(row=1, column=0, padx=(0,10), stick=N+W)
        label3.grid(row=2, column=0, padx=(0,10), stick=N+W)
        self.snakeSpinBox.grid(row=0, column=1, stick=N+W)
        self.snakeSpinBox2.grid(row=1, column=1, stick=N+W)
        self.snakeSpinBox3.grid(row=2, column=1, stick=N+W)
        
        return frame
        
    def validateSpinBox(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        if text in '0123456789':
            try:
                if value_if_allowed == "":
                    return True
                
                value = int(value_if_allowed)
                if value >= 0 and value < 256:
                    return True
                else:
                    return False
            except ValueError:
                return False
            except:
                print "Unexpected error:", sys.exc_info()[0]
        else:
            return False

    def showImage(self, img):
        if img != None:
            label = Label(self, image=img)
            label.image = img  # keep a reference! without it the image will be garbaged
            label.grid(row=1, column=0, sticky=N + W)

    def openFile(self):
        
        fileHandler = tkFileDialog.askopenfile(parent=self, mode='rb', title='Choose the first image')
        if fileHandler != None:
            self.showImage(self.controller.loadImage(fileHandler))
            
            fileHandler2 = tkFileDialog.askopenfile(parent=self, mode='rb', title='Choose the second image')
            if fileHandler2 != None:
                self.showImage(self.controller.loadImage(fileHandler2))

    def setSize(self, w, h):
        
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        
        x = (sw - w) / 2
        y = (sh - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))


def main():
  
    window = Tk()
    interface = Interface(window)
    interface.setSize(900, 600)
    window.mainloop()  

if __name__ == '__main__':
    main()  
