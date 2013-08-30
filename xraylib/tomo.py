import numpy as np

from scipy.fftpack import fft, ifft, fft2, ifft2
from scipy import optimize
from scipy import fftpack
from scipy import ndimage

from skimage import filter as filters

import utils

def sino_remove_bragg_spots(sinogram, block_size=5, tolerance=0.05, sensitivity_low=1.5, sensitivity_high=0.2):
    """ If value is above some local threshold,
        replace by median. Removes dodgy highlights and shadows
        resulting from bragg peaks from large crystallites
        in diffracting orientations """

    # Footprint for median value to replace bragg spots.
    # Usually the spots are contained to one projection,
    # so we sample above and below for good values.
    footprint = np.array(
        [[  False, True, False ],
         [  True,  True,  True ],
         [  False, False, False ],
         [  True,  True,  True ],
         [  False, True, False ]])

    # Only consider pixels which differ from the local median by this offset.
    # Highlights and shadows will skew the arithmetic mean excluding valid line
    # integrals from averaging

    sinogram_high = np.zeros(sinogram.shape)
    sinogram_low  = np.zeros(sinogram.shape)
    sinogram_high[sinogram>0] = sinogram[sinogram>0]
    sinogram_low[sinogram<0] = sinogram[sinogram<0]

    offset_high = np.mean(sinogram[sinogram>0])
    offset_low  = np.mean(sinogram[sinogram<0])

    utils.debug_print(offset_high=offset_high, offset_low=offset_low)

    mask_low = filters.threshold_adaptive(
                sinogram,
                block_size,
                method='median',
                offset=offset_low,
             )
    mask_high = ~filters.threshold_adaptive(
                sinogram,
                block_size,
                method='median',
                offset=offset_high,
             )

    mask = mask_low + mask_high
    if float(mask.sum()) > 0.05 * mask.size:
        #raise RuntimeError(
        print(
                "WARNING: Found more than 5% of values as \
                bragg spots.")
    
    median = ndimage.median_filter(sinogram, footprint=footprint)
    ret = sinogram.copy()
    ret[mask==True] = median[mask==True]
    #return (mask_low, mask_high, ret, median)
    return ret
        
        

def sino_deinterlace(sinogram):
    sino_deinterlaced = sinogram.copy()
    sino_even = sinogram[::2,...]
    sino_odd = sinogram[1::2,...]
    if sino_even.shape > sino_odd.shape:
        shift = _correlate_images(sino_even[:-1,...], sino_odd)
    else:
        shift = _correlate_images(sino_even, sino_odd)

    sino_deinterlaced[1::2,...] = ndimage.shift(sinogram[1::2,...],(0,shift))
    return sino_deinterlaced

def sino_center(sinogram):
    """ Finds rotation axis of sinogram by using first and last projections
    which are assumed to be 180 degrees apart. Last projection is reversed and
    correlated with the first and the shifted image with rotation axis in
    center is returned. """

    proj1 = sinogram[0,...]
    proj2 = sinogram[-1,::-1]
    shift = _correlate_projections(proj1, proj2)
    return ndimage.shift(sinogram, (0,-shift))



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

    def cost_function(s, im1, im2):
        return - np.corrcoef([im1[3:-3, 3:-3].ravel(),
                            ndimage.shift(im2, (0, s))[3:-3, 3:-3].ravel()])[0, 1]
    if method == 'brent':
        newim2 = ndimage.shift(im2, (t0, t1))
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

    def cost_function(s, proj1, proj2):
        cost = - np.corrcoef([proj1, ndimage.shift(proj2,s)])[0,1]
        return cost

    if method == 'brent':
        newproj2 = ndimage.shift(proj2, (t0,))
        refine = optimize.brent(cost_function, args=(proj1, newproj2),
                        brack=[-1, 1], tol=1.e-5)

    return t0 + refine

