#!/usr/bin/env python

import setuptools
from distutils.core import setup

setup(name='MinerUtils',
      version='2.5.5',
      description='GitHub API Access Utilities',
      author='Nicholas Nelson & Caius Brindescu',
      author_email='nelsonni@oregonstate.edu',
      url='https://github.com/EPICLAB/miner-utils',
      packages=['minerutils'],
      install_requires=['requests']
     )
