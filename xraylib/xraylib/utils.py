import os
import xraylib
import numpy as np
from xraylib import files

def strip_none_values(dictionary):
    return dict([ (o,v) for o,v in dictionary.items() if v is not None])

def toFloat(val):
    if hasattr(val, '__iter__'):
        return map(toFloat, val)
    try:
        return float(str(val).strip())
    except ValueError:
        return None

def averageImages(filenames, method='median', verbose=False):
    """ Load and average a list of images. """
    images = [files.ImageFile(f).getImage() for f in filenames if os.path.isfile(f)]
    images = np.array(images)
    if method == 'median':
        return np.median(images,axis=0)
    else:
        raise Exception('NOT IMPLEMENTED')
