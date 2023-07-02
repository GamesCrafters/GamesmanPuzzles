# from distutils.core import setup
from Cython.Build import cythonize
from setuptools import Extension, setup

setup(
    ext_modules=cythonize(
        [Extension("m4ri_utils", ["m4ri_utils.pyx"], extra_compile_args=["-fopenmp"])],
        compiler_directives={"language_level": "3"},
        include_path=["m4ri/"],
    )
)
