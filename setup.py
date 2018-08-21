# The template for this setup.py came from Tim Morton,
#  who I understand took it from Dan F-M. Thanks folks!

# import our ingredients
from setuptools import setup, find_packages
import os,sys

# return the README as a string
def readme():
    with open('README.md') as f:
        return f.read()

# a little kludge to be able to get the version number from the packa
import sys
if sys.version_info[0] < 3:
    import __builtin__ as builtins
else:
    import builtins
builtins.__HENRIETTASETUP__ = True
import thefriendlystars
version = thefriendlystars.__version__

setup(name = "henrietta",
    version = version,
    description = "Python toolkit playing with stellar brightness measurements, for ASTR3400 at CU Boulder.",
    long_description = readme(),
    author = "Zachory K. Berta-Thompson",
    author_email = "zach.bertathompson@colorado.edu",
    url = "https://github.com/zkbt/henrietta",
    packages = find_packages(),
    package_data = {'henrietta':[]},
    include_package_data=False,
    scripts = [],
    classifiers=[
      'Intended Audience :: Science/Research',
      'Programming Language :: Python',
      'Topic :: Scientific/Engineering :: Astronomy'
      ],
    install_requires=['numpy', 'astropy', 'scipy', 'matplotlib'],
    zip_safe=False,
    license='MIT',
)
