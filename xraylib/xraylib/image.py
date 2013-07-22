import numpy as np

def shift(img, count):
    """ Shifts every odd line by a constant number of pixels """
    # TODO subpixel shift, interpolation
    tmp = np.zeros(img.shape,dtype=img.dtype)

    if count == 0:
        return img
    elif count > 0:
        tmp[::2,:-count] = img[::2,count:]
        tmp[1::2,:] = img[1::2,:]
    else:
        count = - count
        tmp[::2,:] = img[::2,:]
        tmp[1::2,:-count] = img[1::2,count:]
    return tmp

def truncate(img, count):
    """ Cut off edges of sinogram. Negative pixel count
    means to truncate right side """
    pass

def sino_center(sinogram):
    pass
