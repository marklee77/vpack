#!/usr/bin/env python
""" Basic Setup Script """

from os import path, system

from setuptools import setup, find_packages
from setuptools.command.install import install

class CustomInstallCommand(install):
    """ Custom Install Command """

    def run(self):
        install.run(self)
        try:
            pass
            # FIXME
            #githash = open('.git/refs/heads/master').read()[:-1]
            #system('sed -i /__GITHASH__/s/__GITHASH__/' + githash + '/ ' +
            #       path.join(self.install_lib, 'vectorpack', 'interface.py'))
        except IOError:
            pass

setup(
    name='VectorPack',
    version='0.1.7',
    description='Vector Packing Heurisitcs',
    author='Mark Stillwell',
    author_email='marklee@fortawesome.org',
    packages=find_packages(),
    include_package_data=True,
    scripts=[
             'bin/pack-vectors', 
             'bin/generate-vectorpack-problem',
             'bin/generate-vectorpack-problem-caprara',
    ],
    url='http://pypi.python.org/pypi/VectorPack/',
    license='LICENSE.txt',
    long_description=open('README.md').read(),
    keywords='',
    classifiers=[
      'Development Status :: 1 - Planning',
      'Intended Audience :: Science/Research',
      'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
      'Topic :: Scientific/Engineering'
    ],
    cmdclass = { 'install' : CustomInstallCommand },
    dependency_links = [
        "https://github.com/mgabay/Variable-Size-Vector-Bin-Packing/tarball/master#egg=vsvbp-0.0.2",
        "https://github.com/fdabrandao/vpsolver/tarball/master#egg=vpsolver-1.1"
    ],
    install_requires = ["pyyaml", "numpy", "vpsolver==1.1", "vsvbp==0.0.2"]
)
