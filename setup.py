from setuptools import setup, Extension

setup(
    name="puzzlesolver",
    version="1.0.0",
    packages=['puzzlesolver'],
    ext_modules=[
        Extension(
            "puzzlesolver._puzzlesolverc", 
            sources=[
                "puzzlesolver/src/Puzzlesolverc.c",

                "puzzlesolver/src/Puzzlec.c",
            ]
        )
    ]
)