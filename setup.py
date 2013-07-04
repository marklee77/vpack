from distutils.core import setup, Command
from distutils.extension import Extension
#from Cython.Distutils import build_ext

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
    version='0.1.5',
    author='Mark Stillwell',
    author_email='marklee@fortawesome.org',
    packages=['vectorpack', 'vectorpack.test'],
    #ext_modules=[Extension("packs", ["vectorpack/packs.py"])],
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
    cmdclass = {'test': PyTest},
    # cmdclass = {'test': PyTest, 'build_ext' : build_ext},
    # install_requires=[ "NumPy" ], FIXME: not supported in distutils?
)
