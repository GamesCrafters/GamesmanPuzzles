#include <Python.h>
#include "util.h"

typedef struct {
    PyObject_HEAD
} Puzzle;

PyTypeObject PuzzleType;

PyObject *Puzzle_new(PyTypeObject *subtype, PyObject *args, PyObject *kwds);
int Puzzle_init(PyObject *self, PyObject *args, PyObject *kwds);
void Puzzle_dealloc(Puzzle *self);

int PyModule_AddPuzzle(PyObject* module);

void PyModule_RemovePuzzle();