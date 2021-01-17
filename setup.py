from setuptools import setup, Extension, find_packages

setup(
    name="example-pkg-ant1ng-puzzlesolver",
    version="1.0.0",
    packages=find_packages(),
    ext_modules=[
        Extension(
            "puzzlesolver.python._puzzlesolverc", 
            sources=[
                "puzzlesolver/c/src/Puzzlesolverc.c",

                "puzzlesolver/c/src/Puzzlec.c",
                "puzzlesolver/c/src/ServerPuzzlec.c",
                
                "puzzlesolver/c/src/Hanoic.c",
                "puzzlesolver/c/src/Hanoi.c"
            ]
        )
    ],
    install_requires=[
        'Flask>=1.1.1',
        'pytest>=5.3.5'
        'sqlitedict>=1.6.0',
        'progressbar2>=3.51.0',
        'networkx>=2.4',
    ]

)