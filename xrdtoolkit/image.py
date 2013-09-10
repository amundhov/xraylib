from scipy.fftpack import fft, ifft, fft2, ifft2
from scipy import optimize
from scipy import fftpack
from scipy import ndimage

import numpy as np

def get_circle_diameter(image, iterations=5):
    #
    image = image > np.median(image) + image.std()*0.85

    # Open image
    image = ndimage.binary_opening(image, iterations=iterations)
    labels,circles = ndimage.label(image)
    ret = []
    for i in xrange(1,circles):
        diameter = sqrt(float(sum(labels[i])) / np.pi) * 2.0

    return labels,circles

# Code taken and adapted from
# https://github.com/eddam/python-esrf/blob/master/rotation_axis.py
# due to Emmanuelle Gouillart

def _correlate_images(im1, im2, method='brent'):
    shape = im1.shape
    f1 = fft2(im1)
    f1[0, 0] = 0
    f2 = fft2(im2)
    f2[0, 0] = 0
    ir = np.real(ifft2((f1 * f2.conjugate())))
    t0, t1 = np.unravel_index(np.argmax(ir), shape)
    if t0 >= shape[0]/2:
        t0 -= shape[0]
    if t1 >= shape[1]/2:
        t1 -= shape[1]

    median2 = np.median(im2)

    def cost_function(s, im1, im2):
        return - np.corrcoef([im1[3:-3, 3:-3].ravel(),
                            ndimage.shift(im2, (0, s),mode='nearest',cval=median2)[3:-3, 3:-3].ravel()])[0, 1]
    if method == 'brent':
        newim2 = ndimage.shift(im2, (t0, t1),mode='nearest',cval=median2)
        refine = optimize.brent(cost_function, args=(im1, newim2),
                        brack=[-1, 1], tol=1.e-2)
    return t1 + refine

def _correlate_projections(proj1, proj2, method='brent'):
    shape = proj1.shape
    f1 = fft(proj1)
    f1[0] = 0
    f2 = fft(proj2)
    f2[0] = 0
    ir = np.real(ifft((f1 * f2.conjugate())))
    (t0,) = np.unravel_index(np.argmax(ir), shape)
    if t0 >= shape[0]/2:
        t0 -= shape[0]

    median2 = np.median(proj2)

    def cost_function(s, proj1, proj2):
        cost = - np.corrcoef([proj1, ndimage.shift(proj2,s,mode='nearest',cval=median2)])[0,1]
        return cost

    if method == 'brent':
        newproj2 = ndimage.shift(proj2, (t0,),mode='nearest',cval=median2)
        refine = optimize.brent(cost_function, args=(proj1, newproj2),
                        brack=[-1, 1], tol=1.e-5)

    return t0 + refine
