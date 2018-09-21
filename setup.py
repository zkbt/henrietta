# The template for this setup.py came from Tim Morton,
#  who I understand took it from Dan F-M. Thanks folks!

# import our ingredients
from setuptools import setup, find_packages
import os,sys

# return the README as a string
def readme():
    with open('README.md') as f:
        return f.read()


# prepare and send a new release to PyPI
if "release" in sys.argv[-1]:
    os.system("python setup.py sdist")
    # uncomment this to test out on test.pypi.com/project/tess-zap
    #os.system("twine upload --repository-url https://test.pypi.org/legacy/ dist/*")
    os.system("twine upload dist/*")
    os.system("rm -rf dist/henrietta*")
    sys.exit()


# a little kludge to be able to get the version number from the packa
import sys
if sys.version_info[0] < 3:
    import __builtin__ as builtins
else:
    import builtins
builtins.__HENRIETTASETUP__ = True
import henrietta
version = henrietta.__version__

setup(name = "henrietta",
    version = version,
    description = "Python toolkit playing with stellar brightness measurements, for ASTR3400 at CU Boulder.",
    long_description = readme(),
    author = "Zach Berta-Thompson",
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
    install_requires=['numpy', 'astropy', 'scipy', 'matplotlib', 'lightkurve'],
    extras_require={'models':['batman-package']},
    zip_safe=False,
    license='MIT',
)
