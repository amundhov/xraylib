#!/usr/bin/env python

import sys,pickle
print ' ---> Exporting X-ray data '
from scipy import io

# Pickle matlab Xray data for use in package

# Transpose matrices saved in matlab to account for row vs column major
xraytable = io.loadmat('xrdtoolkit/data/xraytable.mat', squeeze_me=True, mat_dtype=True, struct_as_record=True)['XrayTable']
for i in range(0,xraytable.shape[0]):
   xraytable['Absorption'][i] = xraytable['Absorption'][i].transpose()
   xraytable['JumpMatrix'][i] = xraytable['JumpMatrix'][i].transpose()

_elements  = io.loadmat('xrdtoolkit/data/elements.mat', squeeze_me=True)['elements']
elements = {}
_count = 1
for element in _elements:
    elements[element.strip()] = _count
    _count += 1

f = open('xrdtoolkit/data/xraytable.pickle','w')
pickle.dump(xraytable,f)
f.close()
f = open('xrdtoolkit/data/elements.pickle','w')
pickle.dump(elements,f)
f.close()
print ' ---> Pickled files written'
