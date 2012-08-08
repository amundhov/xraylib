#!/usr/bin/env python

import sys,pickle
from scipy import io

from setuptools import setup

if len(sys.argv) > 1 and 'bdist_egg' in sys.argv:
    # Pickle matlab Xray data for use in package
    print ' ---> Exporting X-ray data '

    # Transpose matrices saved in matlab to account for row vs column major
    xraytable = io.loadmat('xraytable.mat', squeeze_me=True, mat_dtype=True, struct_as_record=True)['XrayTable']
    for i in xrange(1,xraytable.shape[0]):
        xraytable['Absorption'][i] = xraytable['Absorption'][i].transpose()
        xraytable['JumpMatrix'][i] = xraytable['JumpMatrix'][i].transpose()

    _elements  = io.loadmat('elements.mat', squeeze_me=True)['elements']
    elements = {}
    _count = 1
    for element in _elements:
        elements[element.strip()] = _count
        _count += 1

    f = open('xraylib/data/xraytable','w')
    pickle.dump(xraytable,f)
    f.close()
    f = open('xraylib/data/elements','w')
    pickle.dump(elements,f)
    f.close()

setup(name='xraylib',
      version='0.9',
      description='Xraylib provides routines for calculating cross-sections, form factors and other quantities commonly needed in X-ray experiments',
      package_data = { '' : ['data/*'], },
      #author='Amund Hov',
      #author_email='hov@esrf.fr',
      #url='http://www.python.org/sigs/distutils-sig/',
      packages=['xraylib'],
     )

