import os

class Image:
    def __init__(self,directory,file_name,resource_path='/entry/image'):
        self._extension = os.path.splitext(file_name)[1]
        self._file_path = directory+file_name
        self._resource_path = resource_path
    def getImage(self):
        if self._extension == '.edf':
            import EdfFile
            image = EdfFile.EdfFile(self._file_path).GetData(0)
        elif self._extension == '.h5':
            import h5py
            file = h5py.File(self._file_path)
            image = file[self._resource_path].value
        else:
            raise Exception('Unknown file extension %s' % (self._extension,))
        return image

    def saveImage(self):
        pass
