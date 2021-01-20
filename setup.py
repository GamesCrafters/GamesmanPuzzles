import setuptools
import sys

install_requires = None
ext_modules = None

# CPython extension, (only tested on Linux however)
if sys.platform.startswith('linux'):
    install_requires = [
        'Flask>=1.1.1',
        'pytest>=5.3.5',
        'sqlitedict>=1.6.0',
        'progressbar2>=3.51.0',
        'networkx>=2.4',
    ]
    ext_modules = [
        setuptools.Extension(
            "puzzlesolver._puzzlesolverc", 
            include_dirs=[
                "puzzlesolver/puzzles/hanoi/include",
                "puzzlesolver/include"
            ],
            sources=[
                "puzzlesolver/src/Puzzlesolverc.c",

                "puzzlesolver/src/Puzzlec.c",
                "puzzlesolver/src/ServerPuzzlec.c",
                
                "puzzlesolver/puzzles/hanoi/src/Hanoic.c",
                "puzzlesolver/puzzles/hanoi/src/Hanoi.c"
            ]
        )
    ]

setuptools.setup(
    name="GamesmanPuzzles",
    version="0.0.4",
    packages=setuptools.find_packages(),
    description="A collection of puzzles and solvers under a simple but powerful interface",
    install_requires=install_requires,
    ext_modules=ext_modules,
    python_requires='>=3.6'
)