from numpy import *

#  # HORRIBLE HACK MUST DIE
#  import os, sys, inspect
#  cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
#  #cmd_folder = '/'.join(cmd_folder.split('/')[:-1])
#  if cmd_folder not in sys.path:
#      sys.path.insert(0, cmd_folder)
#      print('FIXME: %s adding %s to system path'%(__name__,cmd_folder))

import xraylib, os
from xraylib import f2w  

try:
    file_name
    file_path
except NameError:
    file_name = 'calibration_image.h5'
    file_path = '/mntdirect/_users/hov/workspace/xray/output/CERN4-REP3/calibration_image.h5'

try:
    image
except NameError:
    # image not given, open calibration file manually
    extension = os.path.splitext(file_name)[1]
    if extension == '.edf':
        import EdfFile
        image = EdfFile(file_path).GetData(0)
    elif extension == '.h5':
        import h5py
        file = h5py.File(file_path)
        image = file['/entry/image'].value
        image = image.squeeze()

# Simple image thresholding to reduce noise
image[image<100] = 0

det = f2w.Perkin()
det.calibrate(image,[10,350])

print(det)

parms = unicode(det)
