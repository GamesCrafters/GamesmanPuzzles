#include "Hanoic.h"
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>
#include <errno.h>

#include <structmember.h>

#define MAX_RODS 20
#define MAX_STR_LEN 220

PyTypeObject HanoicType;

void Hanoi_dealloc(Hanoi *self) {
    deallocateBoard(((Hanoi *) self)->board);
    Py_XDECREF(self->variant);
    Py_TYPE(self)->tp_free(self);
}

PyObject *Hanoi_new(PyTypeObject *subtype, PyObject *args, PyObject *kwds) {
    Hanoi *self = (Hanoi *)subtype->tp_alloc(subtype, 0);
    return (PyObject *)self;
}

int Hanoi_init_empty(PyObject *self, int rod_variant, int disk_variant) {
    Board* start = allocateBoard(disk_variant, rod_variant);
    if (start == NULL) { return -1; }
    ((Hanoi *)self)->board = start;
    ((Hanoi *)self)->disk_variant = disk_variant;
    ((Hanoi *)self)->rod_variant = rod_variant;
    char str[5];
    sprintf(str, "%u_%u", rod_variant, disk_variant);
    ((Hanoi *)self)->variant = PyUnicode_FromString(str);
    ((Hanoi *)self)->max_positions = pow(rod_variant, disk_variant);
    return 0;
}

int Hanoi_init_start(PyObject *self, int rod_variant, int disk_variant) {
    if (Hanoi_init_empty(self, rod_variant, disk_variant) < 0) 
        return -1;
    ((Hanoi *)self)->board->rods[0] = (1 << disk_variant) - 1;
    return 0;
}

int variantid2variant(char* vid, int* rod_variant, int* disk_variant) {
    char buffer[MAX_STR_LEN];
    strcpy(buffer, vid);
    char* token = strtok(buffer, "_");
    if (token == NULL)
        return -1;
    *rod_variant = strtol(token, NULL, 10);

    token = strtok(NULL, "_");
    if (token == NULL)
        return -1;
    *disk_variant = strtol(token, NULL, 10);
    
    if (strtok(NULL, "_") != NULL)
        return -1;
    return 0;
}

// TODO: Accept variantids
int Hanoi_init(PyObject *self, PyObject *args, PyObject *kwds) {
    uint8_t disk_variant, rod_variant;
    disk_variant = 3;
    rod_variant = 3;
    
    char* variantid;
    PyObject* variant;

    // Strange bug, keyword arguments cause seg faults.
    /*
    const char* argnames[] = {"variant", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|O", argnames, &variant)) {
        PyErr_SetString(PyExc_TypeError, "Invalid arguments");
        return -1;
    }
    */
    int err = -1;
    if (kwds != NULL && variant) {
        PyObject* py_disk;
        PyObject* py_rod;
        
        if (!PyDict_Check(variant)) { 
            PyErr_SetString(PyExc_TypeError, "Invalid arguments");
        } else if ((py_disk = PyDict_GetItemString(variant, "disk_variant")) == NULL) {
            PyErr_SetString(PyExc_ValueError, "Variant dict does not contain rod_variant");
        } else if ((py_rod = PyDict_GetItemString(variant, "rod_variant")) == NULL) {
            PyErr_SetString(PyExc_ValueError, "Variant dict does not contain disk_variant");
        } else if (!PyLong_Check(py_disk) || !PyLong_Check(py_rod)) {
            PyErr_SetString(PyExc_TypeError, "Variant dict does not contain proper type");
        } else {
            err = 0;
            disk_variant = PyLong_AsLong(py_disk);
            rod_variant = PyLong_AsLong(py_rod);
        }
    } /* else if (kwds != NULL && variantid) {
        if (variantid2variant(variantid, &rod_variant, &disk_variant) < 0) {
            PyErr_SetString(PyExc_ValueError, "VariantID is not valid");
        } else {
            err = 0;
        }
    } */ else { err = 0; }

    if (err == -1) return -1;
    return Hanoi_init_start(self, rod_variant, disk_variant);
}

void printBoard(PyObject *self, char *str) {
    uint32_t* rods = ((Hanoi *) self)->board->rods;
    uint8_t rod_variant = ((Hanoi *) self)->board->rod_variant;
    for (int i = 0; i < rod_variant; i++) {
        char addend[9];
        snprintf(addend, 9, "%d", rods[i]);
        strncat(str, addend, 9);
        if (i != rod_variant - 1) { strncat(str, "-", 1); }
    }
}

PyObject *Hanoi_repr(PyObject *self) {
    char result[100];
    sprintf(result, "<Puzzle=Hanoi, Board=(");
    printBoard(self, result);
    strcat(result, ")>");
    return PyUnicode_FromString(result);
}

PyObject *Hanoi_str(PyObject *self) {
    char result[100] = "";
    printBoard(self, result);
    return PyUnicode_FromString(result);
}

int highest_bit(int num) {
    int output = 0;
    while (num != 0) {
        num = num >> 1;
        output++;
    }
    return output;
}

int str2rods(char* str, int* rods, int* rod_variant, int* disk_variant) {
    char buffer[MAX_STR_LEN];
    
    strcpy(buffer, str);
    char* token = strtok(buffer, "-");

    if (token == NULL) return -1;
    int i = 0;

    while (token && i < MAX_RODS) {    
        char* endptr = NULL;
        errno = 0;
        int rod = strtol(token, &endptr, 10);

        if (token == endptr)
            return -1;
        if (errno != 0)
            return -2;

        rods[i] = rod;
        int disk = highest_bit(rod);
        if (disk_variant != NULL && *disk_variant < disk) 
            *disk_variant = disk;
        token = strtok(NULL, "-");
        i++;
    }
    if (rod_variant != NULL)
        *rod_variant = i;
    return 0;
}

PyObject *Hanoi_deserialize(PyObject *cls, PyObject *args) {
    char *pid = NULL;
    
    if (!PyArg_ParseTuple(args, "s", &pid)) {
        PyErr_SetString(PyExc_TypeError, "Invalid arguments");
        return NULL;
    }

    int rod_variant = 0;
    int disk_variant = 0;
    int rods[MAX_RODS];

    int err = str2rods(pid, rods, &rod_variant, &disk_variant);
    if (err < 0) {
        PyErr_SetString(PyExc_ValueError, "Could not deserialize argument");
        return NULL;
    }

    Hanoi* self = (Hanoi*) Hanoi_new((PyTypeObject*) cls, NULL, NULL);
    err = Hanoi_init_empty(self, rod_variant, disk_variant);
    if (err == -1) { return -1; }
    for (int i = 0; i < rod_variant; i++) {
        self->board->rods[i] = rods[i];
    }

    return self;
}

int isLegalPosition(char* pid, char* vid) {
    int rod_variant = 0;
    int disk_variant = 0;
    int rods[MAX_RODS];

    int err = str2rods(pid, rods, &rod_variant, &disk_variant);
    if (err < 0) return -1;

    if (vid != NULL) {
        int rod_variant_2 = 0;
        int disk_variant_2 = 0;
        if (variantid2variant(vid, &rod_variant_2, &disk_variant_2) < 0 ||
            rod_variant_2 != rod_variant || disk_variant_2 != disk_variant)
                return -1;
    }

    int sum = 0;
    for (int i = 0; i < rod_variant; i++) {
        sum += rods[i];
    }
    if (sum != (1 << disk_variant) - 1) 
        return -1;
    return 0;
}

PyObject *Hanoi_isLegalPosition(PyObject *cls, PyObject *args, PyObject *kwds) {
    char* pid = NULL; 
    char* vid = NULL;
    static char* argnames[] = {"", "variantid", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "s|s", argnames, &pid, &vid)) {
        PyErr_SetString(PyExc_TypeError, "Invalid arguments");
        return NULL;
    }
    if (isLegalPosition(pid, vid) < 0) {
        Py_RETURN_FALSE;
    }
    Py_RETURN_TRUE;
}

PyObject *Hanoi_generateStartPosition(PyObject *cls, PyObject *args) {
    PyObject *self = Hanoi_new(cls, NULL, NULL);
    int rod_variant = 0;
    int disk_variant = 0;

    char *vid = NULL;
    
    if (!PyArg_ParseTuple(args, "s", &vid)) {
        PyErr_SetString(PyExc_TypeError, "Invalid arguments");
        return NULL;
    }

    if (variantid2variant(vid, &rod_variant, &disk_variant) < 0) {
        PyErr_SetString(PyExc_TypeError, "Invalid variantid");
        return NULL;
    }

    if (Hanoi_init_start(self, rod_variant, disk_variant) < 0) {
        PyErr_SetString(PyExc_AssertionError, "Init didn't work?");
        return NULL;
    }
    return self;
}

PyObject *Hanoi_getName(PyObject *self) {
    return PyUnicode_FromString("Hanoi");
}

PyObject *Hanoi_primitive(PyObject *self) {
    int result = primitive(((Hanoi *) self)->board);
    if (result == 1) {
        return PyUnicode_FromString("SOLVABLE");
    }
    return PyUnicode_FromString("UNDECIDED");
}

PyObject *Hanoi_doMove(PyObject *self, PyObject *args) {
    PyObject *move = NULL;
    if (!PyArg_ParseTuple(args, "O", &move)) {
        PyErr_SetString(PyExc_TypeError, "Invalid arguments");
        return NULL;
    }
    if (move == NULL || !PyTuple_Check(move) || PyTuple_Size(move) != 2) {
        PyErr_SetString(PyExc_TypeError, "Invalid move format");
        return NULL;
    }
    uint8_t start = PyLong_AsLong(PyTuple_GetItem(move, 0));
    uint8_t end = PyLong_AsLong(PyTuple_GetItem(move, 1));

    Board* newBoard = doMove(((Hanoi *) self)->board, (Move) {start, end});
    if (newBoard == NULL) { 
        PyErr_SetString(PyExc_MemoryError, "Memory error or invalid move");
        return NULL; 
    }
    Hanoi* newHanoi = Hanoi_new(&HanoicType, NULL, NULL);
    Hanoi_init_empty(
        newHanoi, 
        ((Hanoi*) self)->rod_variant, 
        ((Hanoi*) self)->disk_variant
    );
    if (newHanoi == NULL) { 
        PyErr_SetString(PyExc_MemoryError, "Memory error");
        deallocateBoard(newBoard); 
        return NULL; 
    }
    newHanoi->board = newBoard;
    return (PyObject*) newHanoi;
}

PyObject *Hanoi_generateMoves(PyObject *self, PyObject *args) {
    uint8_t rod_variant = ((Hanoi *)self)->board->rod_variant;
    Move moves[((rod_variant + 1) * rod_variant) / 2];    
    int num_moves = generateMoves(moves, ((Hanoi *)self)->board, NULL);
    PyObject* move_list = PyList_New(num_moves);
    for (int i = 0; i < num_moves; i++) {
        PyObject* py_move = PyTuple_New(2);
        PyTuple_SetItem(py_move, 0, PyLong_FromDouble(moves[i].start));
        PyTuple_SetItem(py_move, 1, PyLong_FromDouble(moves[i].end));
        PyList_SetItem(move_list, i, py_move);
    }
    return move_list;
}

Py_hash_t *Hanoi_hash(PyObject *self, PyObject *args) {
    return (Py_hash_t) hash(((Hanoi*)self)->board);
}

static PyObject *Hanoi_generateSolutions(PyObject *self) {
    Board* solutions[1];
    int num_sol = generateSolutions(solutions, ((Hanoi*)self)->board);
    if (num_sol < 0) { return NULL; }
    PyObject* list = PyList_New(num_sol);
    PyObject* board = Hanoi_new(&HanoicType, NULL, NULL);
    ((Hanoi*) board)->board = solutions[0];
    PyList_SetItem(list, 0, board);
    return list;
}

PyObject *Hanoi_getSolverClass(PyObject *cls, PyObject *kwds) {
    return PyUnicode_FromString("IndexSolver");
}

PyMemberDef Hanoic_members[] = {
    {"disk_variant", T_INT, offsetof(Hanoi, disk_variant), READONLY, NULL},
    {"rod_variant",  T_INT, offsetof(Hanoi, rod_variant),  READONLY, NULL},
    {"variant", T_OBJECT_EX, offsetof(Hanoi, variant), READONLY, NULL},
    {"numPositions", T_INT, offsetof(Hanoi, max_positions), READONLY, NULL},
    {NULL}
};

PyMethodDef Hanoic_methods[] = {
    {"primitive", (PyCFunction)Hanoi_primitive, METH_NOARGS,
    "Return a primitive"},
    {"doMove", (PyCFunction)Hanoi_doMove, METH_VARARGS,
    "Execute a move on the board"},
    {"generateMoves", (PyCFunction)Hanoi_generateMoves, METH_VARARGS,
    "Generate possible moves"},
    {"generateSolutions", (PyCFunction)Hanoi_generateSolutions, METH_NOARGS,
    "Generate solutions"},
    {"getSolverClass", (PyCFunction)Hanoi_getSolverClass, 
        METH_VARARGS | METH_CLASS | METH_KEYWORDS,
    "Generate recommended Solver class"},
    {"serialize", (PyCFunction)Hanoi_str, METH_VARARGS,
    "Serialize the Puzzle"},
    {"deserialize", (PyCFunction)Hanoi_deserialize, METH_VARARGS | METH_CLASS,
    "Deserialize the Puzzle"},
    {"isLegalPosition", (PyCFunction)Hanoi_isLegalPosition, 
        METH_VARARGS | METH_KEYWORDS | METH_CLASS,
        "Checks if the positionid is a valid puzzle under the rules"
    },
    {"generateStartPosition", (PyCFunction)Hanoi_generateStartPosition,
        METH_VARARGS | METH_CLASS,
        "Creates the starting position of the puzzle"
    },
    {"getName", (PyCFunction)Hanoi_getName,
        METH_VARARGS, 
        "Gets the name of the puzzle for file purposes"},
    {NULL}
};

PyTypeObject HanoicType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "Hanoi",
    .tp_basicsize = sizeof(Hanoi),
    .tp_dealloc = (destructor)Hanoi_dealloc,
    .tp_repr = (reprfunc)Hanoi_repr,
    .tp_hash = (hashfunc)Hanoi_hash,
    .tp_str = (reprfunc)Hanoi_str,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_doc = "hanoic.Hanoi objects",
    .tp_methods = Hanoic_methods,
    .tp_members = Hanoic_members,
    .tp_base = &ServerPuzzleType,
    .tp_init = (initproc)Hanoi_init,
    .tp_new = Hanoi_new
};

static PyObject* name;
static PyObject* puzzleid;
static PyObject* puzzle_name;
static PyObject* description;
static PyObject* date_created;
static PyObject* variants;

int PyModule_AddHanoi(PyObject* module) {
    if (module == NULL) return -1;
    if (PyType_Ready(&HanoicType) < 0) return -1;

    Py_INCREF(&HanoicType);
    PyModule_AddObject(module, "Hanoi", (PyObject *)&HanoicType);
 
    /*
    PyObject* dict = HanoicType.tp_dict;

    // Setting class members in tp_dict. Apparently not safe
    PyObject* author = PyUnicode_FromString("Anthony Ling");
    PyObject* puzzleid = PyUnicode_FromString("hanoi");
    PyObject* name = PyUnicode_FromString("Tower of Hanoi");
    PyObject* description = PyUnicode_FromString(
        "Move smaller discs ontop of bigger discs. Fill the rightmost stack."
    );
    PyObject* date_created = PyUnicode_FromString("April 2, 2020");

    PyDict_SetItemString(dict, "author", author);
    PyDict_SetItemString(dict, "puzzleid", puzzleid);
    PyDict_SetItemString(dict, "name", name);
    PyDict_SetItemString(dict, "description", description);
    PyDict_SetItemString(dict, "date_created", date_created);

    PyObject* variants = PyList_New(0);
    PyObject* test_variants = PyList_New(0);

    PyList_Append(test_variants, PyUnicode_FromString("3_3"));

    PyDict_SetItemString(dict, "variants", variants);
    PyDict_SetItemString(dict, "test_variants", test_variants);

    for (int j = 2; j < 5; j++) {
        for (int i = 1; i <= 14; i++) {
            char buffer[5];
            snprintf(buffer, 5, "%d_%d", j, i);
            PyList_Append(variants, PyUnicode_FromString(buffer));
        }
    }

    Py_XDECREF(name);
    Py_XDECREF(puzzleid);
    Py_XDECREF(name);
    Py_XDECREF(description);
    Py_XDECREF(date_created);
    Py_XDECREF(variants);
    Py_XDECREF(test_variants);
    */
    return 0;
}

void PyModule_RemoveHanoi() {
   Py_XDECREF(&HanoicType);
}