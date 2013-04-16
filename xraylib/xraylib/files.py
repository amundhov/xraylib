import os

import fabio

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
                group = f.require_group(os.path.dirname(data_set))
                dataset = group.require_dataset(
                                name=os.path.basename(data_set),
                                shape=image.shape,
                                dtype=image.dtype
                                )
                dataset[:] = image
        elif self.extension == '.edf':
            import fabio
            edf_image = fabio.edfimage.edfimage(image)
            edf_image.write(self.file_path)

