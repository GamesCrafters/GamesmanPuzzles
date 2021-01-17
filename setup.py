from setuptools import setup, Extension

setup(
    name="example-pkg-ant1ng-puzzlesolver",
    version="1.0.0",
    packages=['puzzlesolver'],
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
    ]
)