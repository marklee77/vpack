#!/usr/bin/env python

from os import path, system

from distutils.core import setup, Command
from distutils.command.install import install
from distutils.extension import Extension

class my_install(install):
    def run(self):
        install.run(self)
        try:
            githash = open('.git/refs/heads/master').read()[:-1]
            system('sed -i /GITHASH/s/GITHASH/' + githash + '/ ' + 
                   path.join(self.install_scripts, 'pack-vectors'))
        except IOError:
            pass

class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        import sys,subprocess
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)

setup(
    name='VectorPack',
    version='0.1.7',
    author='Mark Stillwell',
    author_email='marklee@fortawesome.org',
    packages=['vectorpack', 'vectorpack.test'],
    scripts=[
             'bin/pack-vectors', 
             'bin/generate-vectorpack-problem',
             'bin/generate-vectorpack-problem-caprara',
    ],
    #ext_modules=[Extension("vectorpack.packs", ["vectorpack/packs.pyx"])],
    url='http://pypi.python.org/pypi/VectorPack/',
    license='LICENSE.txt',
    description='Vector Packing Heurisitcs',
    long_description=open('README.txt').read(),
    keywords='',
    classifiers=[
      'Development Status :: 1 - Planning',
      'Intended Audience :: Science/Research',
      'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
      'Topic :: Scientific/Engineering'
    ],
    #cmdclass = {'test': PyTest, 'install': my_install},
    cmdclass = {'install': my_install},
    # install_requires=[ "NumPy" ], FIXME: not supported in distutils?
)
