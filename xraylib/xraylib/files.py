import os

import fabio

class Image:
    def __init__(self,file_path, data_set='/entry/image'):
        self._extension = os.path.splitext(file_path)[1]
        self._file_path = file_path
        self._data_set = data_set
    def getImage(self):
        if self._extension == '.h5':
            import h5py
            with h5py.File(self._file_path) as f:
                self.image = f[self._data_set].value
        else:
            self.image = fabio.openimage.openimage(self._file_path).data
        return self.image

    def saveImage(self, image, data_path='/xraylib/image'):
        """ TODO: implement me """
        if self._extension == '.h5':
            with h5py.File(self.hdf5) as f:
                group = f.require_group(os.path.dirname(self.data_path))

                if os.path.basename(self.data_path) in self.group:
                    self.dataset = self.group[os.path.basename(self.data_path)]
                else:
                    self.dataset = self.group.create_dataset(
                        name=os.path.basename(self.data_path),
                        shape=image.shape,
                        dtype=image.dtype,
                        # TODO, take chunks as parameter
                        chunks=(1, self.nTrans, self.nDiff),
                        maxshape=(None, None, self.nDiff))
