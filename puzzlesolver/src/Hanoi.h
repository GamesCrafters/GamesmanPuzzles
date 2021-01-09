#include "puzzle.h"

struct board {
    uint32_t* rods;
    uint8_t rod_variant;
    uint8_t disk_variant;
};

struct variant {
    uint8_t disk_variant; 
    uint8_t rod_variant;
};

Board* allocateBoard(uint8_t disk_variant, uint8_t rod_variant);