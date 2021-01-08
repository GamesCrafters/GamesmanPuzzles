#include <Python.h>

#include "Puzzlec.h"

static struct PyModuleDef puzzlesolverc = {
    PyModuleDef_HEAD_INIT, "puzzlesolverc",
    "C-extension interface for Puzzlesolver", -1,
    NULL
};

PyMODINIT_FUNC PyInit__puzzlesolverc(void) {
    PyObject* module = PyModule_Create(&puzzlesolverc);

    if (PyModule_AddPuzzle(module) < 0) {
        PyModule_RemovePuzzle();
        return NULL;
    }

    return module;
}