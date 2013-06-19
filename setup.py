#!/usr/bin/env python

from distutils.core import setup

setup(
    name='VPack',
    version='0.1',
    description='Vector Packing Routines',
    author='Mark Stillwell',
    author_email='marklee@fortawesome.org',
    url='',
    license='GPLv3+',
    keywords='',
    packages=['vpack'],
    package_dir = { '' : 'src'},
    long_description=read('README.md')
    classifiers=[
      'Development Status :: 1 - Planning',
      'Intended Audience :: Science/Research',
      'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
      'Topic :: Scientific/Engineering'
    ],
)

