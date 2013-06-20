#!/usr/bin/env python
from os import path
from distutils.core import setup

def read(fname):
    return open(path.join(path.dirname(__file__), fname)).read()

setup(
    name='vpack',
    version='0.1',
    description='Vector Packing Heurisitcs',
    author='Mark Stillwell',
    author_email='marklee@fortawesome.org',
    url='http://packages.python.org/vpack',
    license='GPLv3+',
    keywords='',
    packages=['vpack'],
    package_dir = { '' : 'src'},
    long_description=read('README.md'),
    classifiers=[
      'Development Status :: 1 - Planning',
      'Intended Audience :: Science/Research',
      'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
      'Topic :: Scientific/Engineering'
    ],
)
