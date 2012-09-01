#!/usr/bin/env python

import sys,pickle
from scipy import io

from setuptools import setup

# Pickle matlab Xray data for use in package
print ' ---> Exporting X-ray data '

# Transpose matrices saved in matlab to account for row vs column major
xraytable = io.loadmat('data/xraytable.mat', squeeze_me=True, mat_dtype=True, struct_as_record=True)['XrayTable']
for i in range(0,xraytable.shape[0]):
   xraytable['Absorption'][i] = xraytable['Absorption'][i].transpose()
   xraytable['JumpMatrix'][i] = xraytable['JumpMatrix'][i].transpose()

_elements  = io.loadmat('data/elements.mat', squeeze_me=True)['elements']
elements = {}
_count = 1
for element in _elements:
    elements[element.strip()] = _count
    _count += 1

f = open('data/xraytable.pickle','w')
pickle.dump(xraytable,f)
f.close()
f = open('data/elements.pickle','w')
pickle.dump(elements,f)
f.close()

setup(name='xraylib',
      version='0.9',
      description='Xraylib provides routines for calculating cross-sections, form factors and other quantities commonly needed in X-ray experiments',
      package_data = { '' : ['data/*.pickle'], },
      #author='Amund Hov',
      #author_email='hov@esrf.fr',
      #url='http://www.python.org/sigs/distutils-sig/',
      #packages=['xraylib'],
     )

