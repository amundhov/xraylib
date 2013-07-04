import os
import numpy as np

import fabio

import xraylib

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
                    if xraylib.IMAGE_PATH not in f:
                        raise KeyError('Data set %s does not exist' % (data_set,))
                    else:
                        self.image = f[xraylib.IMAGE_PATH]
        else:
            import fabio
            self.image = fabio.open(self.file_path).data
        return self.image

    def saveImage(self, image, data_set='/xraylib/image'):
        if self.extension == '.h5':
            import h5py
            with h5py.File(self.file_path) as f:
                saveDataset(f, image, data_set)
        elif self.extension == '.edf':
            #FIXME Save multi frames
            if image.ndim > 2:
                raise RuntimeError("Can't save multi-dimensional data sets in edf format")
            import fabio
            edf_image = fabio.edfimage.edfimage(image)
            edf_image.write(self.file_path)

def ImageSequence(file_paths, data_set=xraylib.IMAGE_PATH, group_frames=False):
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


def averageImages(file_paths, method='median'):
    """ Load and average a list of images. """
    if not hasattr(file_paths, '__iter__'):
        file_paths = [ file_paths ]
    file_paths = [ f for f in file_paths if os.path.isfile(f)]
    if len(file_paths) == 0:
        raise Exception("No valid files to average")

    nframes = ImageFile(file_paths[0]).getNFrames()
    image_dims = tuple(ImageFile(file_paths[0]).getImage().shape)
    image_count = len(file_paths)

    edf_files = [ fabio.open(path) for path in file_paths ]
    res = np.zeros((nframes,) + image_dims)
    image_stack = np.zeros((image_count,) + image_dims)
    for i in xrange(0,nframes):
        for j in xrange(0,image_count):
            image_stack[j] = edf_files[j].getframe(i).data
        if method == 'median':
            res[i] = np.median(image_stack,axis=0)
        elif method == 'mean':
            res[i] = np.mean(image_stack,axis=0)
        else:
            raise Exception('METHOD NOT IMPLEMENTED')

    return res.squeeze()
