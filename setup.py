from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize

setup(
    name="GamesmanPuzzles",
    ext_modules=cythonize("puzzlesolver/puzzles/hanoi.pyx"),
    version="0.0.3",
    packages=find_packages(),
    install_requires=[
        "Flask>=1.1.1",
        "pytest>=5.3.5",
        "sqlitedict>=1.6.0",
        "progressbar2>=3.51.0",
        "networkx>=2.4",
    ],
    python_requires=">=3.6",
)