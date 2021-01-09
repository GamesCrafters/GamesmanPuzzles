#include "ServerPuzzlec.h"

PyObject *ServerPuzzle_new(PyTypeObject *subtype, PyObject *args, PyObject *kwds) {
    ServerPuzzle* self = (ServerPuzzle *)subtype->tp_alloc(subtype, 0);
    return (PyObject*) self;
}

int ServerPuzzle_init(PyObject *self, PyObject *args, PyObject *kwds) {
    return 0;
}

void ServerPuzzle_dealloc(ServerPuzzle *self) {
    Py_TYPE(self)->tp_free((PyObject*)self);
}

PyObject* ServerPuzzle_fromString(PyObject* cls, PyObject* args) {
    char* argnames[] = {"", NULL};
    char* positionid;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", argnames, &positionid)) {
        PyErr_SetString(PyExc_TypeError, "PositionID must be type str");
        return NULL;
    }

    if (PyObject_HasAttrString(cls, "isLegalPosition") && 
        PyObject_HasAttrString(cls, "deserialize")) {
        PyObject* bool_output;
        PyObject* string_output;

        PyObject* isLegalPositionObj;
        PyObject* deserializeObj;

        if ((isLegalPositionObj = PyObject_GetAttrString(cls, "isLegalPosition")) == NULL ||
            (bool_output = PyObject_Call(isLegalPositionObj, args, NULL)) == NULL ||
            !PyObject_IsTrue(bool_output) ||
            (deserializeObj = PyObject_GetAttrString(cls, "deserialize")) == NULL ||
            (string_output = PyObject_Call(deserializeObj, args, NULL)) == NULL) {
            PyErr_SetString(PyExc_ValueError, "PositionID could not be translated into a puzzle");
        } 
        Py_XDECREF(bool_output);
        Py_XDECREF(isLegalPositionObj);
        Py_XDECREF(deserializeObj);
        return string_output;
    }
    PyErr_SetString(PyExc_NotImplementedError, "");
    return NULL;
}

PyMethodDef ServerPuzzle_methods[] = {
    {"fromString", (PyCFunction)ServerPuzzle_fromString,
    METH_VARARGS | METH_CLASS,
    "Deserializes a string into a Puzzle"},
    {NULL}
};

PyTypeObject ServerPuzzleType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "Serverpuzzle",
    .tp_basicsize = sizeof(ServerPuzzle),
    .tp_dealloc = (destructor)ServerPuzzle_dealloc,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_doc = "ServerPuzzle objects",
    .tp_methods = ServerPuzzle_methods,
    .tp_base = &PuzzleType,
    .tp_init = (initproc)ServerPuzzle_init,
    .tp_new = ServerPuzzle_new
};

// TODO: Decrement the PyObject references if init fails
int PyModule_AddServerPuzzle(PyObject *module) {
    if (module == NULL) return -1;
    if (PyType_Ready(&ServerPuzzleType) < 0) return -1;

    Py_INCREF(&ServerPuzzleType);
    PyModule_AddObject(module, "ServerPuzzle", (PyObject *)&ServerPuzzleType);

    PyObject* dict = ServerPuzzleType.tp_dict;
    PyObject* list = PyList_New(0);

    PyDict_SetItemString(dict, "variants", list);
    PyDict_SetItemString(dict, "test_variants", list);

    Py_DECREF(list);

    return 0;
}

void PyModule_RemoveServerPuzzle() {
    Py_XDECREF(&ServerPuzzleType);
}