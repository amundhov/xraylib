import os
import numpy as np

import fabio

import xrdtoolkit

EDF = '.edf'
HDF5 = '.h5'
IMAGE_EXTENSIONS = [ EDF, HDF5 ]

def matchImageFiles(path):
    """ Return list of images starting with given path """

    (directory,file_prefix) = os.path.split(os.path.expanduser(path))
    if directory == '':
        directory = '.'
    file_names = [ o for o in os.listdir(directory) if o.startswith(file_prefix) and os.path.splitext(o)[1] in IMAGE_EXTENSIONS]
    return (file_prefix, directory, file_names)

def saveDataset(file_handle, data, data_set='/entry/image'):
    group = file_handle.require_group(os.path.dirname(data_set))
    dataset = group.require_dataset(
                    name=os.path.basename(data_set),
                    shape=data.shape,
                    dtype=data.dtype
                    )
    dataset[:] = data

class ImageFile:
    def __init__(self,file_path):
        self.extension = os.path.splitext(file_path)[1]
        self.file_path = file_path

    def getNFrames(self):
        if self.extension == HDF5:
            return 1
        elif self.extension == EDF:
            return fabio.open(self.file_path).nframes

    def getImage(self, data_set='/entry/image'):
        if self.extension == HDF5:
            import h5py
            with h5py.File(self.file_path) as f:
                try:
                    self.image = f[data_set].value
                except KeyError:
                    if xrdtoolkit.IMAGE_PATH not in f:
                        raise KeyError('Data set %s does not exist' % (data_set,))
                    else:
                        self.image = f[xrdtoolkit.IMAGE_PATH]
        else:
            import fabio
            self.image = fabio.open(self.file_path).data
        return self.image

    def saveImage(self, image, data_set='/xrdtoolkit/image'):
        if self.extension == '.h5':
            import h5py
            with h5py.File(self.file_path) as f:
                saveDataset(f, image, data_set)
        elif self.extension == '.edf':
            import fabio
            edf_image = fabio.edfimage.edfimage()
            if image.ndim == 3:
                edf_image.setData(image[0])
                for i in xrange(1,image.shape[0]):
                    edf_image.appendFrame(data=image[i])
            elif image.ndim > 3:
                raise RuntimeError("Number of dimensions greater than 3.")
            else:
                edf_image.setData(image)
            edf_image.write(self.file_path)

def ImageSequence(file_paths, data_set=xrdtoolkit.IMAGE_PATH, group_frames=False):
    if all([os.path.splitext(file_name)[1] == '.edf' for file_name in file_paths]):
        edf_image = fabio.edfimage.edfimage().read(file_paths[0])
        nframes = edf_image.nframes
        if nframes > 1:
            for f in file_paths:
                edf_image = fabio.open(f)
                if group_frames:
                    ret = np.zeros([edf_image.nframes] + edf_image.dims)
                    for i in xrange(0,edf_image.nframes):
                        ret[i] = edf_image.getframe(i).data
                    yield ret
                else:
                    for i in xrange(0,edf_image.nframes):
                        yield edf_image.getframe(i).data
        else:
            for f in file_paths:
                yield edf_image.fastReadData(f)

    else:
        for f in file_paths:
            yield ImageFile(f).getImage(data_set)


def averageImages(file_paths, method='median', flatten=False):
    """ Load and average a list of images.
        By default multi-frame files maintain their shape,
        that is, frames are averaged across files and not
        over internal frames"""
    if not hasattr(file_paths, '__iter__'):
        file_paths = [ file_paths ]
    file_paths = [ f for f in file_paths if os.path.isfile(f)]
    if len(file_paths) == 0:
        raise Exception("No valid files to average")

    img = ImageFile(file_paths[0]).getImage()
    dtype = img.dtype
    nframes = ImageFile(file_paths[0]).getNFrames()
    image_dims = tuple(img.shape)
    image_count = len(file_paths)

    edf_files = [ fabio.open(path) for path in file_paths ]

    if not flatten:
        res = np.zeros((nframes,) + image_dims, dtype=dtype)
        image_stack = np.zeros((image_count,) + image_dims, dtype=dtype)
        for i in xrange(0,nframes):
            print 'Averaging frame %s' % i
            for j in xrange(0,image_count):
                if nframes == 1:
                    image_stack[j] = edf_files[j].data
                else:
                    image_stack[j] = edf_files[j].getframe(i).data
            if method == 'median':
                res[i] = np.median(image_stack,axis=0).astype(dtype)
            elif method == 'mean':
                res[i] = np.mean(image_stack,axis=0).astype(dtype)
            else:
                raise Exception('METHOD NOT IMPLEMENTED')
    else:
        image_stack = np.array([o for o in ImageSequence(file_paths)])
        if method == 'median':
            res = np.median(image_stack,axis=0).astype(dtype)
        elif method == 'mean':
            res = np.mean(image_stack,axis=0).astype(dtype)
        else:
            raise Exception('METHOD NOT IMPLEMENTED')

    return res.squeeze()
