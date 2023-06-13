import pytest
import json

from puzzlesolver.puzzles import RushHour, PuzzleManager
from puzzlesolver.util import *

# A puzzle of each difficulty
puzzle0 = RushHour.fromString("R_A_0_0_TLRLR-BLR-TTT12-MBBLmRB--T-LR--BLmR---")
puzzle1 = RushHour.fromString("R_A_0_1_LR---TTLmRTMB12-MBTTLRB-BBTLR-LRB-----")
puzzle2 = RushHour.fromString("R_A_0_2_-TLRTT-BTTBM12BBTBLRT-B-T-BT--BLRB----")
puzzle3 = RushHour.fromString("R_A_0_3_T-TLmRM-BTLRB12B-T-T--TM-BLRMBLRLRB---")
puzzle4 = RushHour.fromString("R_A_0_4_TLR-T-MTT-BTBBB12MLmRT-B--TBLRLRBLR---")

# Unit testing
def testHash():
    """Tests the expected behavior of the hash function on the puzzle states. """
    # Note: Hash comparison between different sized boards is undefined

    # A basic solved board has a predictable hash
    puzzle_solved = RushHour.fromString("R_A_0_0_" + "-" * 36 + "12")
    assert hash(puzzle_solved) == 4
    # Two boards should have different hashes
    assert hash(puzzle0) != hash(puzzle2)
    # A board's hash should be decoded back to the original board
    assert RushHour.fromHash("basic", hash(puzzle0)).toString("complex") == puzzle0.toString("complex")
    assert RushHour.fromHash("basic", hash(puzzle1)).toString("complex") == puzzle1.toString("complex")
    assert RushHour.fromHash("basic", hash(puzzle2)).toString("complex") == puzzle2.toString("complex")
    assert RushHour.fromHash("basic", hash(puzzle3)).toString("complex") == puzzle3.toString("complex")
    assert RushHour.fromHash("basic", hash(puzzle4)).toString("complex") == puzzle4.toString("complex")
