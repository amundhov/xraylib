from skimage import filter as filters
from scipy import ndimage

import numpy as np

import utils, image

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
    # Highlights and shadows will skew the arithmetic mean so use median.

    median_value = np.median(sinogram)
    offset_high  = np.median(sinogram[sinogram>median_value])
    offset_low   = np.median(sinogram[sinogram<median_value])

    utils.debug_print(median=median_value,offset_high=offset_high, offset_low=offset_low)

    mask_low = ~filters.threshold_adaptive(
                 sinogram,
                 block_size,
                 method='median',
                 offset=-sensitivity_low*(offset_low-median_value),
             )
    mask_high = filters.threshold_adaptive(
                 sinogram,
                 block_size,
                 method='median',
                 offset=-sensitivity_high*(offset_high-median_value),
             )
    if float(mask_high.sum()) > tolerance * mask_high.size:
        # Too many values marked as spots. Ignoring hilights.
        print('Found more than %s%% of values as hilights' % (tolerance * 100))
        mask_high = np.zeros(shape=sinogram.shape, dtype=bool)
    if float(mask_low.sum()) > tolerance * mask_low.size:
        # Too many values marked as spots. Ignoring shadows.
        print('Found more than %s%% of values as shadows' % (tolerance * 100))
        mask_low = np.zeros(shape=sinogram.shape, dtype=bool)

    mask = mask_low + mask_high
    # FIXME, only calculate values in mask.
    median = ndimage.median_filter(sinogram, footprint=footprint)
    ret = sinogram.copy()
    ret[mask==True] = median[mask==True]
    return ret
    #return (median_value, offset_high, offset_low, mask_low, mask_high, median, ret)
        

def sino_deinterlace(sinogram):
    sino_deinterlaced = sinogram.copy()
    sino_even = sinogram[::2,...]
    sino_odd = sinogram[1::2,...]
    if sino_even.shape > sino_odd.shape:
        shift = image._correlate_images(sino_even[:-1,...], sino_odd)
    else:
        shift = image._correlate_images(sino_even, sino_odd)

    sino_deinterlaced[1::2,...] = ndimage.shift(sinogram[1::2,...],(0,shift),mode='nearest')
    return sino_deinterlaced

def sino_center(sinogram):
    """ Finds rotation axis of sinogram by using first and last projections
    which are assumed to be 180 degrees apart. Last projection is reversed and
    correlated with the first and the shifted image with rotation axis in
    center is returned. """

    proj1 = sinogram[0,...]
    proj2 = sinogram[-1,::-1]
    shift = image._correlate_projections(proj1, proj2)
    return ndimage.shift(sinogram, (0,-shift), mode='nearest',cval=np.median(sinogram))


