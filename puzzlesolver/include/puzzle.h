#include <stdint.h>
#include <stdlib.h>

typedef struct board Board;
typedef struct move {
    uint8_t start;
    uint8_t end;
} Move;
typedef struct variant Variant;

int primitive(Board *state);
Board* doMove(Board *state, Move move);

Board* generateStartPosition(Variant* puzzle_variant);
int generateMoves(Move *moves, Board *state, char *dir);
int generateSolutions(Board **solutions, Board *state);

int maxMoves(Board *state);
int maxSolutions(Board *state);

int hash(Board *state);
int deallocateBoard(Board *state);
