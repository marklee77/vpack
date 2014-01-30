#!/usr/bin/env python
""" Basic Setup Script """

from os import path, system

from setuptools import setup
from setuptools.command.install import install

class CustomInstallCommand(install):
    """ Custom Install Command """

    def run(self):
        install.run(self)
        try:
            githash = open('.git/refs/heads/master').read()[:-1]
            system('sed -i /__GITHASH__/s/__GITHASH__/' + githash + '/ ' +
                   path.join(self.install_lib, 'vectorpack', 'interface.py'))
        except IOError:
            pass

setup(
    name='VectorPack',
    version='0.1.7',
    description='Vector Packing Heurisitcs',
    author='Mark Stillwell',
    author_email='marklee@fortawesome.org',
    packages=['vectorpack', 'vectorpack.test'],
    include_package_data=True,
    scripts=[
             'bin/pack-vectors', 
             'bin/generate-vectorpack-problem',
             'bin/generate-vectorpack-problem-caprara',
    ],
    url='http://pypi.python.org/pypi/VectorPack/',
    license='LICENSE.txt',
    long_description=open('README.txt').read(),
    keywords='',
    classifiers=[
      'Development Status :: 1 - Planning',
      'Intended Audience :: Science/Research',
      'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
      'Topic :: Scientific/Engineering'
    ],
    cmdclass = { 'install' : CustomInstallCommand }
)
