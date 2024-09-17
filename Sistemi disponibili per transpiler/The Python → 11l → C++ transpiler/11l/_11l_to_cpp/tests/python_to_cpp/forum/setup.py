#from distutils.core import setup
from setuptools import setup
from Cython.Build import cythonize

setup(
    #ext_modules = cythonize("exs2sfz.pyx"), zip_safe=False
    ext_modules = cythonize("prime2.pyx"), zip_safe=False
)
