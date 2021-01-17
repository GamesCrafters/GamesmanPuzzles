#include "uthash.h"
#include "utstack.h"
#include "util.h"
#include <stdio.h>
#include <Python.h>

typedef struct entry {
    int id;            /* we'll use this field as the key */
    int remoteness;
    UT_hash_handle hh; /* makes this structure hashable */
} Entry;

typedef struct el {
    PyObject* data;
    struct el *next;
} PyEntry;

int getCount(Entry** entries) {
    return HASH_COUNT(*entries);
}

Entry** init() {
    Entry** ptr = malloc(sizeof(Entry*));
    *ptr = NULL;
    return ptr;
}

int setRemoteness(Entry** entries, int hash, int remoteness) {
    struct entry *entry;
    entry = malloc(sizeof(struct entry));
    if (entry == NULL) return -1;
    entry->id = hash;
    entry->remoteness = remoteness;
    HASH_ADD_INT( *entries, id, entry );
    return 0;
}

int setRemotenessPyObject(Entry** entries, PyObject* obj, int remoteness) {
    int hash = PyObject_Hash(obj);
    return setRemoteness(entries, hash, remoteness);
}

int getRemoteness(Entry** entries, int hash) {
    struct entry *s;

    HASH_FIND_INT( *entries, &hash, s );
    if (s == NULL) return -1;
    return s->remoteness;
}

int getRemotenessPyObject(Entry** entries, PyObject* obj) {
    int hash = PyObject_Hash(obj);
    return getRemoteness(entries, hash);
}

int clear(Entry** entries) {
    struct entry *entry, *tmp;
    HASH_ITER(hh, *entries, entry, tmp) {
        HASH_DEL(*entries, entry);
        free(entry);
    }
    free(*entries);
    return 0;
}

int solve(Entry** entries, PyObject* puzzle) {
    if (puzzle == NULL) return -1;
    Py_XINCREF(puzzle);

    PyObject* solutions = NULL;
    PyObject* moves = NULL;
    PyObject* primitive = NULL;

    PyObject* newPuzzle = NULL;

    PyEntry* stack = NULL;

    if ((solutions = PyObject_CallMethod(puzzle, "generateSolutions", NULL)) == NULL)
        goto err;

    Py_XDECREF(puzzle);
    for (int i = 0; i < PyList_Size(solutions); i++) {
        puzzle = PyList_GetItem(solutions, i);
        if (puzzle == NULL) goto err;
        Py_XINCREF(puzzle);
        setRemotenessPyObject(entries, puzzle, 0);

        PyEntry* entry = malloc(sizeof(PyEntry));
        entry->data = puzzle;
        STACK_PUSH(stack, entry);
    }
    Py_CLEAR(solutions);

    while (stack != NULL) {
        PyEntry* entry = NULL;
        STACK_POP(stack, entry);

        puzzle = entry->data;
        free(entry);

        int remoteness = getRemotenessPyObject(entries, puzzle);
        // TODO: This is probably wrong, "undo" is supposed to be in a tuple
        if ((moves = PyObject_CallMethod(puzzle, "generateMoves", "s", "undo")) == NULL)
            goto err;

        for (int i = 0; i < PyList_Size(moves); i++) {
            PyObject* move = NULL;
            move = PyList_GetItem(moves, i);
            if (move == NULL) goto err;

            PyObject* args = PyTuple_New(1);
            PyTuple_SetItem(args, 0, move);
            if ((newPuzzle = PyObject_CallMethod(puzzle, "doMove", "O", args)) == NULL)
                goto err;
            Py_CLEAR(args);
            if (getRemotenessPyObject(entries, newPuzzle) == -1) {
                setRemotenessPyObject(entries, newPuzzle, remoteness + 1);
                
                entry = malloc(sizeof(PyEntry));
                entry->data = newPuzzle;
                STACK_PUSH(stack, entry);
            } else {
                Py_CLEAR(newPuzzle);
            }
        }
        Py_CLEAR(moves);
        Py_CLEAR(puzzle);
    }

    return 0;

err:
    Py_XDECREF(puzzle);
    Py_XDECREF(solutions);
    Py_XDECREF(moves);
    Py_XDECREF(primitive);
    Py_XDECREF(newPuzzle);
    Py_XDECREF(stack);
    return -1;
}