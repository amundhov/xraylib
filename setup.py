#!/usr/bin/env python

try:
    from setuptools import setup
except:
    from distutils.core import setup
import os, sys, glob

script_files = glob.glob("scripts/*")
install_requires=[ o.strip('\n') for o in open('requirements.txt').readlines() if not '#' in o]

setup(name='xrdtoolkit',
      version='0.9',
      description='xrdtoolkit provides routines for calculating cross-sections, form factors and other quantities commonly needed in X-ray experiments',
      install_requires=install_requires,
      package_data = { 'xrdtoolkit' : ['data/*.pickle'], },
      include_package_data=True,
      packages=['xrdtoolkit'],
      scripts=script_files,
      test_suite='tests',
      author='Amund Hov',
      author_email='amund.hov@esrf.fr',
      url='http://www.python.org/sigs/distutils-sig/',
     )

