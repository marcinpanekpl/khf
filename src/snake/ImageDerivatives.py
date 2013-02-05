from __future__ import division
import Image
import sys
from numpy.ma import power
import pylab
import scipy

__author__ = 'Marcin'

import numpy as np
import math
from scipy.signal import convolve2d
from scipy import ndimage as ndi

def gauss_x(x, y, sigma):
    return -(x/(2*math.pi*sigma**4)) * power(math.exp(1),-(x**2+y**2)/(2*sigma**2))

def gauss_y(x, y, sigma):
    return 1/(2*math.pi*sigma**4) * (x**2/sigma**2 - 1) * power(math.exp(1), -(x**2 + y**2)/(2*sigma**2))

def gauss_xx(x, y, sigma):
    return 1/(2*math.pi*sigma**4) * (x**2/sigma**2 - 1) * power(math.exp(1), -(x**2 + y**2)/(2*sigma**2))

def gauss_xy(x, y, sigma):
    return 1/(2*math.pi*sigma**6) * (x * y)           * power(math.exp(1), -(x**2 + y**2)/(2*sigma**2))

def gauss_yy(x, y, sigma):
    return 1/(2*math.pi*sigma**4) * (y**2/sigma**2 - 1) * power(math.exp(1), -(x**2 + y**2)/(2*sigma**2))

def dispatch(value, x, y, sigma):
    thismodule = sys.modules[__name__]
    method_name = 'gauss_' + str(value)
    method = getattr(thismodule, method_name)
    return method(x, y, sigma)

def imageDerivatives(I,sigma,type):
    x, y = np.mgrid[math.floor(-3*sigma):math.ceil(3*sigma)+1,math.floor(-3*sigma):math.ceil(3*sigma)+1]
    DGauss = dispatch(type, x, y, sigma)
#    print DGauss

#    J = ndi.convolve(I,DGauss,mode='mirror');
    J = convolve2d(I, DGauss, 'same', 'symm')
    return J

if __name__ == '__main__':
    result = Image.open("../image3.bmp")
    array = result.convert("L")
    imageDerivatives(array, 8, 'xy')
