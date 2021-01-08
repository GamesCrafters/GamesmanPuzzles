#include <Python.h>

typedef struct {
    PyObject_HEAD
} Puzzle;

PyTypeObject PuzzleType;

int PyModule_AddPuzzle(PyObject* module);

void PyModule_RemovePuzzle();