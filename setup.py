from setuptools import setup, Extension, find_packages

setup(
    name="GamesmanPuzzles",
    version="0.0.3",
    packages=find_packages(),
    install_requires=[
        'Flask>=1.1.1',
        'pytest>=5.3.5',
        'sqlitedict>=1.6.0',
        'progressbar2>=3.51.0',
        'networkx>=2.4',
    ],
    ext_modules=[
        Extension(
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
    ],
    python_requires='>=3.6'
)