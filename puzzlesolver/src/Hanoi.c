#include "Hanoi.h"
#include <strings.h>

int primitive(Board *state) {
    return state->rods[state->rod_variant - 1] == (1 << state->disk_variant) - 1;
}

Board* generateStartPosition(Variant* puzzle_variant) {
    uint8_t disk_variant = puzzle_variant->disk_variant;
    uint8_t rod_variant = puzzle_variant->rod_variant;
    Board* board = allocateBoard(disk_variant, rod_variant);
    if (board == NULL) {
        return NULL;
    }
    board->rods[0] = (1 << disk_variant) - 1;
    return board;
}

Board* doMove(Board *state, Move move) {
    uint8_t start = move.start;
    uint8_t end = move.end;
    
    if (start >= state->rod_variant || end >= state->rod_variant) 
        return NULL;
    
    uint32_t startRod = state->rods[start];
    uint32_t endRod = state->rods[end];

    // Can only make a move if the index of the LSB of the start rod is less
    // than the LSB of the end rod. 
    // Consider the LSB of 0 as infinite.
    if (startRod == 0 || (endRod != 0 && ffs(startRod) > ffs(endRod)))
        return NULL;

    uint8_t i = ffs(startRod) - 1;

    Board* newBoard = allocateBoard(state->disk_variant, state->rod_variant);
    if (newBoard == NULL) {
        return NULL;
    }
    
    newBoard->rods[start] = startRod ^ (1 << i);
    newBoard->rods[end] = endRod | (1 << i);
    for (int j = 0; j < state->rod_variant; j++) {
        if (j != start && j != end)
            newBoard->rods[j] = state->rods[j];
    }

    newBoard->rod_variant = state->rod_variant;
    newBoard->disk_variant = state->disk_variant;
    return newBoard;
}

int generateMoves(Move *moves, Board *state, char *dir) {
    int num_moves = 0;
    for (int i = 0; i < state->rod_variant; i++) {
        for (int j = i + 1; j < state->rod_variant; j++) {
            int i_index, j_index;
            i_index = ffs(state->rods[i]);
            j_index = ffs(state->rods[j]);
            if (i_index == 0 && j_index == 0) { continue; }
            if (i_index == 0 && j_index != 0) {
                moves[num_moves] = (Move) { j, i };
                num_moves++;
            } 
            if (i_index != 0 && j_index == 0) {
                moves[num_moves] = (Move) { i, j };
                num_moves++;
            }
            if (i_index != 0 && j_index != 0) {
                if (i_index > j_index) {
                    moves[num_moves] = (Move) { j, i };
                    num_moves++;
                }
                if (i_index < j_index) {
                    moves[num_moves] = (Move) { i, j };
                    num_moves++;
                }
            }
        }
    }
    return num_moves;
}

int maxMoves(Board *state) {
    return state->rod_variant;
}

int maxSolutions(Board *state) {
    return 1;
}

uint32_t* ordering;

int cmp(const void *a, const void *b) {
    int ia = *(int *)a;
    int ib = *(int *)b;
    return (ordering[ia] > ordering[ib]) - (ordering[ia] < ordering[ib]);
}

int hash(Board *state) {
    uint32_t* rods = state->rods;
    uint8_t disk_variant = state->disk_variant;
    uint8_t rod_variant = state->rod_variant;

    int ffs_bits[rod_variant - 1];
    int order[rod_variant - 1];

    for (int i = 0; i < rod_variant - 1; i++) {
        ffs_bits[i] = ffs(rods[i]) == 0 ? disk_variant : ffs(rods[i]);
        order[i] = i;
    }
    ordering = ffs_bits;
    qsort(order, rod_variant - 1, sizeof(*order), cmp);

    int output = 0;
    int mask = 1;
    for (int j = 0; j < disk_variant; j++) {
        output *= rod_variant;
        for (int i = rod_variant - 2; i >= 0; i--) {
            output += ((rods[order[i]] >> j) & mask) * (i + 1);
        }
    }
    return output;
}

int generateSolutions(Board **solutions, Board *state) {
    uint8_t disk_variant = state->disk_variant;
    uint8_t rod_variant = state->rod_variant;
    Board* sol = allocateBoard(disk_variant, rod_variant);
    if (sol == NULL) { return -1; }
    *solutions = sol;
    sol->rods[rod_variant - 1] = (1 << disk_variant) - 1;
    return 1;
}

Board* allocateBoard(uint8_t disk_variant, uint8_t rod_variant) {
    Board* result = malloc(sizeof(Board));
    if (result == NULL) { return NULL; }
    result->rods = calloc(rod_variant, sizeof(uint32_t));
    if (result->rods == NULL) { free(result); return NULL; }
    result->rod_variant = rod_variant;
    result->disk_variant = disk_variant;
    return result;
}

int deallocateBoard(Board *state) {
    free(state->rods);
    free(state);
    return 1;
}