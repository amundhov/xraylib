import os
import numpy as np

import fabio

def saveDataset(file_handle, data, data_set='/xraylib/image'):
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
    def getImage(self, data_set='/entry/image'):
        if self.extension == '.h5':
            import h5py
            with h5py.File(self.file_path) as f:
                self.image = f[self.data_set].value
        else:
            import fabio
            self.image = fabio.openimage.openimage(self.file_path).data
        return self.image

    def saveImage(self, image, data_set='/xraylib/image'):
        """ TODO: implement me """
        if self.extension == '.h5':
            import h5py
            with h5py.File(self.file_path) as f:
                saveDataset(f, image, data_set)
        elif self.extension == '.edf':
            import fabio
            edf_image = fabio.edfimage.edfimage(image)
            edf_image.write(self.file_path)

def ImageSequence(file_names):
    if all([os.path.splitext(file_name)[1] == '.edf' for file_name in file_names]):
        edf_image = fabio.edfimage.edfimage().read(file_names[0])
        for f in file_names:
            yield edf_image.fastReadData(f)
    else:
        for f in file_names:
            yield ImageFile(f).getImage()

# TODO write test
def averageImages(file_names, method='median'):
    """ Load and average a list of images. """
    file_names = [ f for f in file_names if os.path.isfile(f)]
    if len(file_names) == 0:
        raise Exception("No valid files to average")

    images = np.dstack([ o for o in ImageSequence(file_names)])

    if method == 'median':
        return np.median(images,axis=2)
    elif method == 'mean':
        return np.mean(images,axis=2)
    else:
        raise Exception('METHOD NOT IMPLEMENTED')
