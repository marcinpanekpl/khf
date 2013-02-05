from __future__ import division
from math import cos, sin, pi
import Image
import ImageDraw
import numpy as np
import pylab
from scipy.interpolate import RectBivariateSpline
from src.ImageHandler import ImageHandler
from pylab import *
from ExternalForce import externalForce, optimizeImageForces
from ImageDerivatives import imageDerivatives
from scipy import ndimage as ndi

__author__ = 'Marcin'


def array2PIL(arr, size):
    mode = 'RGBA'
    arr = arr.reshape(arr.shape[0]*arr.shape[1], arr.shape[2])
    if len(arr[0]) == 3:
        arr = np.c_[arr, 255*np.ones((len(arr),1), np.uint8)]
    return Image.frombuffer(mode, size, arr.tostring(), 'raw', mode, 0, 1)

def circularShift(seq, n):
    n %= len(seq)
    return np.vstack((seq[-n:], seq[:-n]))

def getContourNormals2D(P):
    # Use the n'th neighbour to calculate the normal (more stable)
    a=4

    # From array to separate x,y
    xt=P[:,1]
    yt=P[:,2]

    # Derivatives of contour
    n=len(xt)
    f=np.arange(n+1)+a; f[f > n] -= n
    b=np.arange(n+1)-a; b[b<1] += n;

    dx=xt[f]-xt[b];
    dy=yt[f]-yt[b];

    # Normals of contourpoints
    l=np.sqrt(dx**2+dy**2);
    nx = -dy/l;
    ny =  dx/l;
    N[:,1]=nx; N[:,2]=ny;

def moveIteration(S, P, Fext, gamma, kappa, delta):
    Fext1 = []

    # Clamp contour to boundary
#    P[]:,1] = min(max(P(:,1),1),size(Fext,1))
#    P(:,2)=min(max(P(:,2),1),size(Fext,2))
    P[:,0] = minimum(maximum(P[:,0],1),Fext.shape[0])
    P[:,1] = minimum(maximum(P[:,1],1),Fext.shape[1])

    # Get image force on the contour points
#    Fext1(:,1)=kappa*interp2(Fext(:,:,1),P(:,2),P(:,1));
#    Fext1(:,2)=kappa*interp2(Fext(:,:,2),P(:,2),P(:,1));
    I = RectBivariateSpline(Fext[:,:,1], Fext[:,:,1], Fext[:,:,1], kind='linear')  # TODO TEST IT !!!
    Fext1[:,0] = kappa * I(P[:,1], P[:,0])
    Fext1[:,1] = kappa * I(P[:,1], P[:,0])

    # Calculate the baloonforce on the contour points
    N=getContourNormals2D(P);
    Fext2=delta*N;

    # Update contour positions
    ssx = gamma*P[:,0] + Fext1[:,1] + Fext2[:,1]
    ssy = gamma*P[:,1] + Fext1[:,2] + Fext2[:,2]
    P[:,0] = S * ssx
    P[:,1] = S * ssy

    # Clamp contour to boundary
    P[:,0] = minimum(maximum(P[:,0],1),Fext.shape[0])
    P[:,1] = minimum(maximum(P[:,1],1),Fext.shape[1])

def generateInnerForceMatrix(nPoints, alpha, beta, gamma):
    b = np.empty(nPoints)
    A = np.zeros((nPoints,nPoints))

    # Penta diagonal matrix, one row:
    b[1]=beta
    b[2]=-(alpha + 4*beta)
    b[3]=(2*alpha + 6 *beta)
    b[4]=b[2]
    b[5]=b[1]

    # Make the penta matrix (for every contour point)
    A=b[1]*circularShift(eye(nPoints),2);
    A=A+b[2]*circularShift(eye(nPoints),1);
    A=A+b[3]*circularShift(eye(nPoints),0);
    A=A+b[4]*circularShift(eye(nPoints),-1);
    A=A+b[5]*circularShift(eye(nPoints),-2);

    # Calculate the inverse
    return inv(A + gamma * eye(nPoints)) # TODO moze byc odwrocona

def exampleVF():
    X,Y = meshgrid( arange(0,2*pi,.2),arange(0,2*pi,.2) )
    U = cos(X)
    V = sin(Y)

    figure()
    Q = quiver( X, Y, U, V, units='width')
    qk = quiverkey(Q, 0.9, 0.95, 2, r'$2 \frac{m}{s}$',
        labelpos='E',
        coordinates='figure',
        fontproperties={'weight': 'bold'})
    axis([-1, 7, -1, 7])
    title('scales with plot width, not view')
    show()

def snake(img, P, options):

    # Transform the Image into an External Energy Image
#    Eext = externalForce(img, options['wLine'], options['wEdge'], options['wTerm'],options['sigma1']);
    Eext = ndi.gaussian_filter(img,options['sigma1'])

#    imshow(Eext)
#    gray()
#    show()

    # Make the external force (flow) field.
    Fx=imageDerivatives(Eext,options['sigma2'],'x');
    Fy=imageDerivatives(Eext,options['sigma2'],'y');
    Fext= np.dstack( (-Fx*2*options['sigma2']**2, -Fy*2*options['sigma2']**2 ) )

    optimizeImageForces(Fext, options['mu'], options['gIterations'], options['sigma3'])

#    figure()
#    quiver(Fext[0], Fext[1])
#    show()


    S = generateInnerForceMatrix(options['nPoints'], options['alpha'], options['beta'], options['gamma'])
#    print S

    # Main loop
    for i in range(len(P)):

        moveIteration(S,P,Fext,options['gamma'],options['kappa'],options['delta'])
        if options['verbose']:
            tmpImg = img.copy()
            for point in P:
                ImageHandler().putBigRedPoint(tmpImg, point, 2, (184, 3, 255))
            imshow(np.asarray(tmpImg))

def initContour((left, upper, right, lower), numPoints):
    P = []
    step = (right - left + lower - upper) * 2 // numPoints

    y = upper
    for x in range(left, right, step):
        P.append((x,y))

    x = right
    for y in range(upper, lower, step):
        P.append((x,y))

    y = lower
    for x in range(right, left, -step):
        P.append((x,y))

    x = left
    for y in range(lower, upper, -step):
        P.append((x,y))

    return np.array(P)


if __name__ == '__main__':

    img = Image.open("../image3.bmp")
    photo = img.copy().convert("RGB")
    img = img.convert("L")

#    center = (287, 232)
    box = (200,70,400,400) # original values (11,73,403,390)
#    draw = ImageDraw.Draw(photo)
#    #    draw.rectangle(box, outline="red")
#    ImageHandler().putBigRedPoint(photo, center)
#
    P = initContour(box, 100)
#
#    for point in P:
#        ImageHandler().putBigRedPoint(photo, point, 2, (184, 3, 255))
#
#    photo.show()


    options = dict(
        verbose=True,
        nPoints=100,
        wEdge=2,
        wLine=0,
        wTerm=0,
        alpha=0.1,
        beta=0.1,
        delta=-0.1,
        gamma=1,
        kappa=4,
        sigma1=8,
        sigma2=8,
        sigma3=1,
        mu=0.2,
        iterations=100,
        gIterations=100)

    snake(img, P, options)


