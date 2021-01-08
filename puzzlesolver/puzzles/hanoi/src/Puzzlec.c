#include "Puzzlec.h"

PyObject *Puzzle_new(PyTypeObject *subtype, PyObject *args, PyObject *kwds) {
    Puzzle* self = (Puzzle *)subtype->tp_alloc(subtype, 0);
    return (PyObject*) self;
}

int Puzzle_init(PyObject *self, PyObject *args, PyObject *kwds) {
    return 0;
}

void Puzzle_dealloc(Puzzle *self) {
    Py_TYPE(self)->tp_free((PyObject*)self);
}

PyObject *Puzzle_str(PyObject *self) {
    return PyUnicode_FromString("(No String representation available)");
}

int getFunctionPointerFromAttr(
    PyObject *self, PyCFunction *func, const char *str, const char *err) 
{
    if (PyObject_HasAttrString(self, str)) {
        PyObject* obj = PyObject_GetAttrString(self, str);
        *func = PyCFunction_GetFunction(obj);
        Py_DECREF(obj);
    } else {
        PyErr_SetString(PyExc_AttributeError, err);
        return -1;
    }
    return 0;
}  

PyObject *Puzzle_printInfo(PyObject *self) {
    FILE* fp = stdout;
    if (PyObject_Print(self, fp, Py_PRINT_RAW) < 0) {
        PyErr_SetString((PyObject*)PyErr_BadInternalCall, "Print fails?");
        return NULL;
    }
    printf("\n");
    Py_RETURN_NONE;
}

PyObject *Puzzle_generateSolutions(PyObject *self) {
    return PyList_New(0);
}

PyObject *Puzzle_generateMovePositions(PyObject *self, PyObject *args, PyObject *kwds) {
    int err = -1;
    PyObject* generateMoves;
    PyObject* moves;
    PyObject* doMove;
    PyObject* puzzles = PyList_New(0);

    if ((generateMoves = PyObject_GetAttrString(self, "generateMoves")) == NULL) {
        PyErr_SetString(PyExc_AttributeError, "generateMoves not found");
        goto END;
    }
    if (!PyCallable_Check(generateMoves)) {
        PyErr_SetString(PyExc_TypeError, "generateMoves is not callable");
        goto END;
    } 
    if ((moves = PyObject_Call(generateMoves, args, kwds)) == NULL) {
        PyErr_SetString(PyExc_TypeError, "generateMoves didn't return expected");
        goto END;
    }

    if ((doMove = PyObject_GetAttrString(self, "doMove")) == NULL) {
        PyErr_SetString(PyExc_AttributeError, "doMove not found");
        goto END;
    }
    if (!PyCallable_Check(doMove)) {
        PyErr_SetString(PyExc_TypeError, "doMove is not callable");
        goto END;
    }
    for (Py_ssize_t i = 0; i < PyList_GET_SIZE(moves); i++) {
        PyObject* move = PyList_GetItem(moves, i);
        PyObject* puzzle = PyObject_CallFunctionObjArgs(doMove, move, NULL);

        if (puzzle == NULL) {
            PyErr_BadInternalCall();
            goto END;
        }

        PyObject* movePuzzle = PyList_New(0);
        if (movePuzzle == NULL) {
            PyErr_BadInternalCall();
            goto END;
        }
        PyList_Append(movePuzzle, move);
        PyList_Append(movePuzzle, puzzle);

        PyList_Append(puzzles, movePuzzle);
    }
    err = 0;

END: 
    Py_XDECREF(generateMoves);
    Py_XDECREF(moves);
    Py_XDECREF(doMove);
    if (err < 0) {
        Py_XDECREF(puzzles);
        return NULL;
    }
    return puzzles;
}

PyMethodDef Puzzle_methods[] = {
    {"generateMovePositions", (PyCFunction)Puzzle_generateMovePositions, 
    METH_VARARGS,
    "Return move positions"},
    {"printInfo", (PyCFunction)Puzzle_printInfo,
    METH_NOARGS,
    "Prints puzzle info"},
    {"generateSolutions", (PyCFunction)Puzzle_generateSolutions,
    METH_NOARGS,
    "Default generateSolutions"},
    {NULL}
};

PyTypeObject PuzzleType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "Puzzle",
    .tp_basicsize = sizeof(Puzzle),
    .tp_dealloc = (destructor)Puzzle_dealloc,
    .tp_str = (reprfunc)Puzzle_str,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_doc = "Puzzle objects",
    .tp_methods = Puzzle_methods,
    .tp_init = (initproc)Puzzle_init,
    .tp_new = Puzzle_new,    
};

static PyObject* numPositions;
static PyObject* puzzleid;
static PyObject* puzzle_name;
static PyObject* author;
static PyObject* description;
static PyObject* date_created;
static PyObject* variants;

int PyModule_AddPuzzle(PyObject* module) {
    if (PyType_Ready(&PuzzleType) < 0) return -1;
    
    Py_INCREF(&PuzzleType);
    if (PyModule_AddObject(module, "Puzzle", (PyObject *)&PuzzleType) < 0)
        return -1;

    PyObject* dict = PuzzleType.tp_dict;
    numPositions = PyFloat_FromDouble(-1);
    puzzleid = PyUnicode_FromString("N/A");
    puzzle_name = PyUnicode_FromString("N/A");
    author = PyUnicode_FromString("N/A");
    description = PyUnicode_FromString("N/A");
    date_created = PyUnicode_FromString("N/A");
    variants = PyList_New(0);

    PyDict_SetItemString(dict, "numPositions", numPositions);
    PyDict_SetItemString(dict, "puzzleid", puzzleid);
    PyDict_SetItemString(dict, "puzzle_name", puzzle_name);
    PyDict_SetItemString(dict, "author", author);
    PyDict_SetItemString(dict, "description", description);
    PyDict_SetItemString(dict, "date_created", date_created);
    PyDict_SetItemString(dict, "variants", variants);
    PyDict_SetItemString(dict, "test_variants", variants);
    
    return 0;
}

void PyModule_RemovePuzzle() {
    Py_XDECREF(numPositions);
    Py_XDECREF(puzzleid);
    Py_XDECREF(puzzle_name);
    Py_XDECREF(author);
    Py_XDECREF(description);
    Py_XDECREF(date_created);

    Py_XDECREF(&PuzzleType);
}