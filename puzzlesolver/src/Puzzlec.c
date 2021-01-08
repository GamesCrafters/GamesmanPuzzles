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

PyObject* Puzzle_variant(PyObject *self, void* closure) {
    return PyUnicode_FromString("NA");
}

PyObject* Puzzle_toString(PyObject *self, PyObject *args, PyObject *kwds) {
    char* mode = "minimal";
    char* argnames[] = {"mode", NULL};

    PyObject* output;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|s", argnames, &mode)) {
        PyErr_SetString(PyExc_TypeError, "Invalid arguments");
        return NULL;
    }

    if (strcmp("minimal", mode) == 0 && PyObject_HasAttrString(self, "serialize")) {
        if ((output = PyObject_CallMethod(self, "serialize", NULL)) == NULL) {
            return NULL;
        }
    }
    else if (strcmp("complex", mode) == 0 && PyObject_HasAttrString(self, "printInfo")) {
        if ((output = PyObject_CallMethod(self, "printInfo", NULL)) == NULL) {
            return NULL;
        }
    }
    else {
        return PyObject_Str(self);
    }
    return output;
}

PyObject* Puzzle_numPositions(PyObject *self, void* closure) {
    Py_RETURN_NONE;
}

PyObject* Puzzle_generateSolutions(PyObject* self) {
    return PyList_New(0);
}

PyMethodDef Puzzle_methods[] = {
    {"toString", (PyCFunction)Puzzle_toString,
    METH_VARARGS | METH_KEYWORDS,
    "Return string representation"},
    {"generateSolutions", (PyCFunction)Puzzle_generateSolutions,
    METH_NOARGS,
    "Return the solutions of the Puzzle"},
    {NULL}
};

PyGetSetDef Puzzle_getset[] = {
    {"variant", (getter)Puzzle_variant, 
    NULL, "Get the variant of the Puzzle",
    NULL},
    {"numPositions", (getter)Puzzle_numPositions,
    NULL, "Get the numPositions of the Puzzle",
    NULL}, 
    {NULL}
};
 
PyTypeObject PuzzleType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "Puzzle",
    .tp_basicsize = sizeof(Puzzle),
    .tp_dealloc = (destructor)Puzzle_dealloc,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_doc = "Puzzle objects",
    .tp_methods = Puzzle_methods,
    .tp_getset = Puzzle_getset,
    .tp_init = (initproc)Puzzle_init,
    .tp_new = Puzzle_new,    
};

int PyModule_AddPuzzle(PyObject* module) {
    if (PyType_Ready(&PuzzleType) < 0) return -1;
    
    Py_INCREF(&PuzzleType);
    if (PyModule_AddObject(module, "Puzzle", (PyObject *)&PuzzleType) < 0)
        return -1;

    PyObject* dict = PuzzleType.tp_dict;
    PyObject* NA = PyUnicode_FromString("NA");

    PyDict_SetItemString(dict, "puzzleid", NA);
    PyDict_SetItemString(dict, "author", NA);
    PyDict_SetItemString(dict, "name", NA);
    PyDict_SetItemString(dict, "description", NA);
    PyDict_SetItemString(dict, "date_created", NA);
    
    Py_DECREF(NA);

    return 0;
}

void PyModule_RemovePuzzle() {
    Py_XDECREF(&PuzzleType);
}