# HORRIBLE HACK MUST DIE
import os, sys, inspect
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
print(cmd_folder)
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
    print('FIXME: %s adding %s to system path'%(__name__,cmd_folder))

from time import time
start = time()
import numpy as np

import xraylib
import xraylib.files
from xraylib import f2w

try:
    file_prefix = file_prefix
    directory = file_dir
except NameError:
    #FIXME MOCK PARAMETERS - REMOVE
    file_prefix = 'CERN4-REP3_000'
    directory = '/data/id15/inhouse/Olof/CERN4-REP3_000/'

# FIXME - use file import in workbench when
# http://jira.diamond.ac.uk/browse/DAWNSCI-305 is fixed
dark_file_name = 'dark_current.h5'
dark_file_dir = '/mntdirect/_users/hov/workspace/xray/output/CERN4-REP3/'

dark_current = xraylib.files.Image(dark_file_dir,dark_file_name,'/entry/data/amplitude').getImage()

print('Dark current dimension: %s' % (dark_current.shape))

files = [ o for o in os.listdir(directory) if o.startswith(file_prefix) ]
images = [ xraylib.files.Image(directory,o) for o in files ]

# Assuming file names NAME_xxx_yyy_zzz.hd5
# Get range of parameters x,y,z
# splitext removes any file extension.
parms = [ [int(parm) for parm in os.path.splitext(o)[0].split('_')[1:]]  for o in files ]
parmsT = np.array(parms).T

dimensions = parmsT.shape[0]
print('Number of parameters: %s' % dimensions)

print(parmsT)

min_indices = parmsT.argmin(axis=1)
max_indices = parmsT.argmax(axis=1)

parm_range = [ ( parmsT[i][min_indices[i]], parmsT[i][max_indices[i]] ) for i in xrange(0,dimensions) ]
parm_size  = [ 1+max-min for min,max in parm_range ]

print '%f seconds finding parms' % (time()-start)

det = f2w.Perkin()
# FIXME: Get calibration from configfile or similar
det.setorigin(np.array([ 197.20634855,  211.88283524]))
det.settilt(np.array([ -0.18697419,  0.0135755]))

result = det.integrate(images[0].getImage())

output = np.zeros(tuple(parm_size)+result[1].squeeze().shape)
output[tuple(parms[0])] = result[1].squeeze()
radius = result[0].squeeze()

print('Assembling %s' % (output.shape,)) 

start = time()
for i in xrange(1,len(files)):
     # Integrate and save azimuthal amplitude only
     result = det.integrate(images[i].getImage())
     result = result[1].squeeze() - dark_current
     output[tuple(parms[i])] = result
     print('Parameters   %s' % (parms[i],))
     print('Integrating  %s' % (files[i]))
     print('Time used %s' % (time()-start)) 

# TODO: Preserve axes if parameters are not null indexed.
