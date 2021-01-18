#include "Hanoi.h"
#include "ServerPuzzlec.h"
#include <Python.h>

#define MAX_MOVE_SPACE 3

typedef struct {
    ServerPuzzle super; 
    Board *board;
    int disk_variant;
    int rod_variant;
    int max_positions;
    PyObject *variant;
} Hanoi;

int PyModule_AddHanoi(PyObject* module);

void PyModule_RemoveHanoi();