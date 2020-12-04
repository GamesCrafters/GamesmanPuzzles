from copy import deepcopy
from . import ServerPuzzle
from ..util import *
from ..solvers import IndexSolver
from ..solvers import GeneralSolver
from ..solvers import SqliteSolver

class Klotski(ServerPuzzle):
    puzzleid = 'klotski'
    variants = {
        '1': GeneralSolver
    }
    def __init__(self, v = 1, **kwargs):
        """
        blocks maps position to type for each position
        type: 1 for RED, 2 for 1x1, 3 for 2x1
        position: numbered starting from 0 from top left
        :param kwargs:
        """
        self.blocks = {} # position to block
        if v == 1:
            self.blocks[0] = Block(1, 1)
            self.blocks[1] = Block(0, 0)
            self.blocks[3] = Block(2, 1)
            self.blocks[4] = Block(3, 1)
            for i in range(4, 14):
                b = Block(i, 1)
                self.blocks[i + 3] = b
            self.blocks[19] = Block(14, 1)
        """
        Official variant 
        self.blocks[0] = Block(1, 2)
        self.blocks[1] = Block(0, 0)
        self.blocks[3] = Block(2, 2)
        self.blocks[8] = Block(3, 2)
        self.blocks[9] = Block(4, 3)
        self.blocks[11] = Block(5, 2)
        self.blocks[13] = Block(6, 1)
        self.blocks[14] = Block(7, 1)
        self.blocks[16] = Block(8, 1)
        self.blocks[19] = Block(9, 1)
        """

    def __str__(self,**kwargs):
        lst = [' _ |']*20
        for i in self.blocks:
            type = self.blocks[i].type
            if self.blocks[i].id < 10:
                lst[i] = ' ' + str(self.blocks[i].id) + ' |'
            else:
                lst[i] = str(self.blocks[i].id) + ' |'
            if type == 0:
                lst[i] = '   0'
                lst[i+1] = '   |'
                lst[i+4] = '    '
                lst[i+5] = '   |'
            if type == 2:
                lst[i+4] = '  |'
        for i in range(20,0,-4):
            lst[i-1] = lst[i-1][:-1]
            lst.insert(i, '\n')
        return ''.join(lst)

    def __hash__(self):
        # see design doc
        h = [9]*20
        for i in self.blocks:
            type = self.blocks[i].type
            if type == 0:
                h[i] = type
                h[i+1] = type
                h[i+4] = type
                h[i+5] = type
            elif type == 1:
                h[i] = type
            elif type == 2:
                h[i] = type
                h[i+4]= type
            elif type == 3:
                h[i] = type
                h[i+1] = type
        return int(''.join(str(i) for i in h))

    def primitive(self, **kwargs):
        # just check if block is in final position
        if 13 in self.blocks and self.blocks[13].id == 0:
            return PuzzleValue.SOLVABLE
        return PuzzleValue.UNDECIDED

    def findEmpties(self):
        filled = set(range(20))
        for i in self.blocks:
            b = self.blocks[i]
            if b.type == 0:
                filled -= {i, i+1, i+4, i+5}
            elif b.type == 1:
                filled.remove(i)
            elif b.type == 2:
                filled -= {i, i+4}
            elif b.type == 3:
                filled -= {i, i+1}
        return filled

    def generateMoves(self, movetype = 'all', **kwargs):
        # a move is (block id, u/d/l/r)
        # for each block and each direction, get the positions it will move to and check if they are empty blocks
        if movetype == 'for' or movetype == 'back': return []
        moves = []
        empties = self.findEmpties()
        for i in self.blocks:
            b = self.blocks[i]
            if b.type == 1:
                up = [i-4]
                down = [i+4]
                left = [i-1]
                right = [i+1]
            elif b.type == 0:
                up = [i-4, i-3]
                down = [i+8, i+9]
                left = [i-1, i+3]
                right = [i+2, i+6]
                if i % 4 == 2:
                    right = [-1]
                if i % 4 == 1:
                    left = [-1]
            elif b.type == 2: #2x1
                up = [i - 4]
                down = [i + 4]
                left = [i - 1, i +3]
                right = [i + 1, i+5]
                if i % 4 == 2:
                    right = [-1]
                if i % 4 == 1:
                    left = [-1]
            elif b.type == 3: # 1x2
                up = [i-4, i-3]
                down = [i+4, i+5]
                left = [i-1]
                right =[i+2]
                if i % 4 == 2:
                    right = [-1]
                if i % 4 == 1:
                    left = [-1]
            if i % 4 == 0:
                left = [-1]
            if i % 4 == 3:
                right = [-1]
            if all([n in empties for n in up]):
                moves.append((self.blocks[i].id, 'u'))
            if all([n in empties for n in down]):
                moves.append((self.blocks[i].id, 'd'))
            if all([n in empties for n in left]):
                moves.append((self.blocks[i].id,'l'))
            if all([n in empties for n in right]):
                moves.append((self.blocks[i].id, 'r'))
        return moves

    def doMove(self, move, *kwargs):
        # move block
        # relabel all the blocks
        # change the empties appropriately
        if move not in self.generateMoves():
            raise ValueError
        newPuzzle = Klotski()
        blocks = deepcopy(self.blocks)
        id = move[0]
        dir = move[1]
        for i in blocks: # find position of block with given id
            if blocks[i].id == id:
                curr_position = i
                break
        block = blocks.pop(curr_position)
        if dir == 'u':
            blocks[curr_position-4] = block
        elif dir == 'd':
            blocks[curr_position+4] = block
            if block.type == 0:
                newPuzzle.blocks = blocks
        elif dir == 'l':
            blocks[curr_position - 1] = block
        elif dir == 'r':
            blocks[curr_position + 1] = block

        count = 1
        for i in range(20):
            if i in blocks and blocks[i].id != 0:
                blocks[i].id = count
                count += 1
        newPuzzle.blocks = blocks
        return newPuzzle

    def generateSolutions(self, **kwargs):
        # fix the red block and push around the empties
        solns = []
        blocks = {}
        for i in list(range(13)) + [15, 16, 19]:
            blocks[i] = Block(1,1)
        blocks[13] = Block(0, 0)


        poss_empties = [[9,10], [12,16], [15,19]]
        for pair in poss_empties:
            b = deepcopy(blocks)
            b.pop(pair[0])
            b.pop(pair[1])
            count = 1
            for k in range(20):
                if k in b and b[k].id != 0:
                    b[k].id = count
                    count += 1
            newPuzzle = Klotski()
            newPuzzle.blocks = b
            solns.append(newPuzzle)
        return solns

    @property
    def variant(self):
        return '1'

    def serialize(self, **kwargs):
        h = [9]*20
        for i in range(20):
            if i in self.blocks:
                h[i] = self.blocks[i].type
        """
        h = [9]*20
        for i in self.blocks:
            type = self.blocks[i].type
            id = self.blocks[i].id
            if type == 0:
                h[i] = id
                h[i + 1] = id
                h[i + 4] = id
                h[i + 5] = id
            elif type == 1:
                # h[i] = id
            elif type == 2:
                h[i] = id
                h[i + 4] = id
            elif type == 3:
                h[i] = id
                h[i + 1] = id
        """
        return ''.join(str(i) for i in h)

    @classmethod
    def deserialize(cls, positionid, **kwargs):
        if not positionid.isnumeric or len(positionid) != 20:
            raise PuzzleException
        blocks = {}
        for i in range(len(positionid)):
            if positionid[i] != '9':
                blocks[i] = Block(0, int(positionid[i]))
        count = 1
        for k in range(20):
            if k in blocks and blocks[k].type != 0:
                blocks[k].id = count
                count += 1
        puzzle = Klotski()
        puzzle.blocks = blocks
        return puzzle

    @classmethod
    def isLegalPosition(cls, positionid, variantid=None, **kwargs):
        try: puzzle = cls.deserialize(positionid)
        except: return False
        if len(puzzle.findEmpties()) != 2:
            return False
        return True

    @classmethod
    def generateStartPosition(cls, variantid, **kwargs):
        if not isinstance(variantid, str): raise TypeError("Invalid variantid")
        if variantid not in Klotski.variants: raise IndexError("Out of bounds variantid")
        return Klotski(variant = int(variantid))

class Block:
    def __init__(self, id, type):
        """
        :param type: 0 for RED, 1 for 1x1, 2 for 2x1
        :param position: position of top left, numbered starting from 0 from top left
        """
        self.id = id
        self.type = type

    def __str__(self):
        return str(self.id, self.type)

    def __repr__(self):
        return str(self.id) + ' ' + str(self.type)