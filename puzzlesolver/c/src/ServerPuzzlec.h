#include <Python.h>

#include "Puzzlec.h"

typedef struct {
    Puzzle super;
} ServerPuzzle;

PyTypeObject ServerPuzzleType;

int PyModule_AddServerPuzzle(PyObject* module);

void PyModule_RemoveServerPuzzle();