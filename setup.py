from distutils.core import setup

setup(
    name='VectorPack',
    version='0.1.1',
    author='Mark Stillwell',
    author_email='marklee@fortawesome.org',
    packages=['vectorpack', 'vectorpack.test'],
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
)
