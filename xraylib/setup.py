#!/usr/bin/env python

from setuptools import setup


setup(name='xraylib',
      version='0.9',
      description='Xraylib provides routines for calculating cross-sections, form factors and other quantities commonly needed in X-ray experiments',
      package_data = { 'xraylib' : ['data/*.pickle'], },
      include_package_data=True,
      packages=['xraylib'],
      test_suite='tests',
      install_requires=['numpy'],
      author='Amund Hov',
      author_email='amund.hov@esrf.fr',
      url='http://www.python.org/sigs/distutils-sig/',
     )

