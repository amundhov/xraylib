import numpy as np

import xraylib, os
from xraylib import f2w,files

try:
    base_name
    directory = file_dir
except NameError:
    #FIXME MOCK PARAMETERS - intregrate with workbench
    base_name = 'DARK_CERN4-REP3_000'
    directory = '/data/id15/inhouse/Olof/CERN4-REP3_000/'

files = [ files.Image(directory,o) for o in os.listdir(directory) if o.startswith(base_name) ]

image = files[0].getImage().squeeze()
images = np.zeros((len(files),) + image.shape)

print(images.shape)

from time import time
start = time()

for i in xrange(0,len(files)):
    images[i] = files[i].getImage()
    print('%s of %s images loaded' % (i+1,len(files),))

print('%s seconds used' % (time()-start))

# FIXME Refactor script to require calibrated detector object
det = f2w.Perkin()
det.setorigin(np.array([ 197.20634855,  211.88283524]))
det.settilt(np.array([ -0.18697419,  0.0135755]))

print('--> Performing median')
start = time()
dark_current = np.median(images,axis=0)
print('%s seconds used' % (time()-start))

print('--> Integrating ')
start = time()
(radius, amplitude)= det.integrate(dark_current)
radius = radius.flatten()
amplitude = amplitude.flatten()
print('%s seconds used' % (time()-start))
