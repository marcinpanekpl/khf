from __future__ import division
from ImageDerivatives import *

__author__ = 'Marcin'

def externalForce(img, wLine, wEdge, wTerm, sigma):
    """
    input:
    img     : The image
    wLine   : Attraction to lines, if negative to black lines otherwise white lines
    wEdge   : Attraction to edges
    wTerm   : Attraction to terminations of lines (end points) and corners
    sigma   : Sigma used to calculated image derivatives

    output:
            The energy function described by the image
    """

    Ix= imageDerivatives(img,sigma,'x')
    Iy=imageDerivatives(img,sigma,'y')
    Ixx=imageDerivatives(img,sigma,'xx')
    Ixy=imageDerivatives(img,sigma,'xy')
    Iyy=imageDerivatives(img,sigma,'yy')


    eLine = ndi.gaussian_filter(img,sigma)
    eTerm = (Iyy * Ix**2 -2*Ixy * Ix * Iy + Ixx * Iy**2)/((1+Ix**2 + Iy**2)**(3/2))
    eEdge = np.sqrt(Ix**2 + Iy**2)

    return  wLine*eLine - wEdge*eEdge - wTerm * eTerm


def optimizeImageForces(Fext, mu, iterations, sigma):
    """
    inputs:
    Fext : The image force vector field N x M x 2
    Mu : Is a trade of scalar between noise and real edge forces
    Iterations : The number of GVF itterations
    Sigma : Used when calculating the Laplacian

    outputs:
    Fext : The GVF optimized image force vector field
    """

    Fx= Fext[0]
    Fy= Fext[1]

    sMag = Fx**2+ Fy**2

    u=Fx
    v=Fy

    for i in range(iterations):
        Uxx=imageDerivatives(u,sigma,'xx')
        Uyy=imageDerivatives(u,sigma,'yy')

        Vxx=imageDerivatives(v,sigma,'xx')
        Vyy=imageDerivatives(v,sigma,'yy')

        u = u + mu*(Uxx+Uyy) - sMag*(u-Fx)
        v = v + mu*(Vxx+Vyy) - sMag*(v-Fy)

    return np.dstack((u,v))
