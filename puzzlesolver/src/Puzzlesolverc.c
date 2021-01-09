#include <Python.h>

#include "Hanoic.h"

static struct PyModuleDef puzzlesolverc = {
    PyModuleDef_HEAD_INIT, "puzzlesolverc",
    "C-extension interface for Puzzlesolver", -1,
    NULL
};

PyMODINIT_FUNC PyInit__puzzlesolverc(void) {
    PyObject* module = PyModule_Create(&puzzlesolverc);

    if (PyModule_AddPuzzle(module) < 0 ||
        PyModule_AddServerPuzzle(module) < 0 ||
        PyModule_AddHanoi(module) < 0) {
        PyModule_RemovePuzzle();
        PyModule_RemoveServerPuzzle();
        PyModule_RemoveHanoi();
        return NULL;
    }

    return module;
}