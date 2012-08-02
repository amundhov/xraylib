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
from xraylib.f2w import Pixium

try:
    base_name = file_name
    directory = file_dir
except NameError:
    #FIXME MOCK PARAMETERS - REMOVE
    base_name = 'CERN4-REP3_000'
    directory = '/data/id15/inhouse/Olof/CERN4-REP3_000/'

# Extract experiment parameters from filename.
# splitext removes any file extension, and the rest of the 
files = [ o for o in os.listdir(directory) if o.startswith(base_name) ]
filetype = os.path.splitext(files[0])[1]
parms = [ os.path.splitext(o)[0].split('_')[1:] for o in files ]
parms = np.array(parms).T

dimensions = parms.shape[0]

min_indices = parms.argmin(axis=1)
max_indices = parms.argmax(axis=1)

parm_range = [ ( int(parms[i][min_indices[i]]), int(parms[i][max_indices[i]]) ) for i in xrange(0,dimensions) ]
parm_size  = [ 1+max-min for min,max in parm_range ]

print '%f seconds finding parms' % (time()-start)


print 'Assembling'
output = np.zeros(tuple(parm_size))
