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
    """Tests the expected behavior of the hash function on the puzzle states."""
    # Note: Hash comparison between different sized boards is undefined

    # The same board should always have the same hash
    puzzle0_v2 = RushHour.fromString("R_A_0_0_TLRLR-BLR-TTT12-MBBLmRB--T-LR--BLmR---")
    assert hash(puzzle0_v2) == hash(puzzle0)
    # Two boards should have different hashes
    assert hash(puzzle0) != hash(puzzle2)
    # A board's hash should be decoded back to the original board
    assert RushHour.fromHash("basic", hash(puzzle0)).toString("complex") == puzzle0.toString("complex")
    assert RushHour.fromHash("basic", hash(puzzle1)).toString("complex") == puzzle1.toString("complex")
    assert RushHour.fromHash("basic", hash(puzzle2)).toString("complex") == puzzle2.toString("complex")
    assert RushHour.fromHash("basic", hash(puzzle3)).toString("complex") == puzzle3.toString("complex")
    assert RushHour.fromHash("basic", hash(puzzle4)).toString("complex") == puzzle4.toString("complex")

def testPrimitive():
    """Tests that primitive positions are correctly detected."""
    assert puzzle0.primitive() == PuzzleValue.UNDECIDED
    assert puzzle1.primitive() == PuzzleValue.UNDECIDED
    assert puzzle2.primitive() == PuzzleValue.UNDECIDED
    assert puzzle3.primitive() == PuzzleValue.UNDECIDED
    assert puzzle4.primitive() == PuzzleValue.UNDECIDED

    solved_puzzle = RushHour.fromString("R_A_0_0_" + "-" * 36 + "12")
    assert solved_puzzle.primitive() == PuzzleValue.SOLVABLE
    solved_puzzle = RushHour.fromString("R_A_0_0_" + "LRLR--" * 6 + "12")
    assert solved_puzzle.primitive() == PuzzleValue.SOLVABLE
    solved_puzzle = RushHour.fromString("R_A_0_0_" + "LRLR--" * 2 + "LRLR12" + "LRLR--" * 3)
    assert solved_puzzle.primitive() == PuzzleValue.SOLVABLE
def testMoves():
    """Tests that moves are correctly generated and performed."""
    assert set(puzzle0.generateMoves()) == {'M_18_24', 'M_11_5', 'M_4_5', 'M_8_9', 'M_17_23', 'M_17_29',
         'M_17_35', 'M_27_26', 'M_28_29', 'M_18_30', 'M_14_15', 'M_34_35'}

    # 2-length piece moves - up/down
    new_puzzle0 = puzzle0.doMove('M_18_30')
    assert hash(new_puzzle0) == hash(RushHour.fromString("R_A_0_0_TLRLR-BLR-TT-12-MB-LmRB-TT-LR-BBLmR---"))
    reset_puzzle0 = new_puzzle0.doMove('M_24_12')
    assert hash(reset_puzzle0) == hash(puzzle0)

    # 2-length piece moves - right/left
    new_puzzle0 = new_puzzle0.doMove('M_14_15')
    assert hash(new_puzzle0) == hash(RushHour.fromString("R_A_0_0_TLRLR-BLR-TT--12MB-LmRB-TT-LR-BBLmR---"))
    new_puzzle0 = new_puzzle0.doMove('M_14_12')
    assert hash(new_puzzle0) == hash(RushHour.fromString("R_A_0_0_TLRLR-BLR-TT12--MB-LmRB-TT-LR-BBLmR---"))

    # 3-length piece moves - left/right
    new_puzzle0 = puzzle0.doMove('M_34_35')
    assert hash(new_puzzle0) == hash(RushHour.fromString("R_A_0_0_TLRLR-BLR-TTT12-MBBLmRB--T-LR--B-LmR--"))
    new_puzzle0 = new_puzzle0.doMove('M_33_32')
    assert hash(new_puzzle0) == hash(puzzle0)

    # 3-length piece moves - up/down
    assert set(puzzle1.generateMoves()) == {'M_17_23', 'M_17_29', 'M_1_2', 'M_1_4', 'M_10_4', 'M_1_3',
         'M_17_35', 'M_28_29', 'M_14_15'}
    new_puzzle1 = puzzle1.doMove('M_17_35')
    assert hash(new_puzzle1) == hash(RushHour.fromString("R_A_0_1_LR----TLmRT-B12-M-TTLRBTBBTLRMLRB--B--"))
    new_puzzle1 = new_puzzle1.doMove('M_23_5')
    assert hash(new_puzzle1) == hash(puzzle1)

    # Test that moves to/from winning positions are correctly pointing outside the board
    basic_puzzle = RushHour.fromString("R_A_0_0_" + "-" * 12 + "12----" + "-" * 18 + "--")
    assert set(basic_puzzle.generateMoves()) == {f"M_13_{i}" for i in [14, 15, 16, 36]}

    solved_puzzle = basic_puzzle.doMove("M_13_36")
    assert hash(solved_puzzle) == hash(RushHour.fromString("R_A_0_0_" + "-" * 36 + "12"))
    assert hash(solved_puzzle) == hash(RushHour.fromString("R_A_0_0_" + "-" * 12 + "----12" + "-" * 20))
    assert set(solved_puzzle.generateMoves()) == {f"M_36_{i}" for i in [12, 13, 14, 15]}

    assert hash(solved_puzzle.doMove("M_36_12")) == hash(basic_puzzle)
