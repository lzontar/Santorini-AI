import json
import random
import warnings

from django.http import HttpResponse

from .lib import setupBlankBoard


class Santorini():
    def __init__(self):
        self.board = setupBlankBoard()
        self.wipe()
        self.cols = ['Red', 'Blue']
        self.turn = 0
        self.player = self.cols[self.turn % 2]
        self.algAI = 'Random move AI'

    # To be called to change the currently active player.
    # This parameter is used for correct player move verification.
    def setPlayer(self):
        self.player = self.cols[self.turn % 2]

    # Proceeds to the next turn. Parameter is used to determine which player
    # can move.
    def nextTurn(self):
        self.turn += 1

    def makeRandomMove(self):
        options = self.getAllCurrentAvailableMoves()
        if not options:
            return False
        move = random.choice(options)
        self.move(move[0], move[1])
        return move

    def makeRandomBuild(self, _to):
        options = self.getAvailableBuilds(_to)
        b = random.choice(options)
        self.build(b)
        return b

    def makeAIMove(self):
        if self.algAI == 'Random move/build AI':
            return self.makeRandomMove()
        if self.algAI == 'Highest move':
            return self.makeRandomMove()
        if self.algAI == 'Highest move and build':
            return self.makeMoveHighest()
        if self.algAI == 'Heuristics 2143':
            return self.makeMove2143()
        
    def makeAIBuild(self, _to):
        if self.algAI == 'Random move/build AI':
            return self.makeRandomBuild(_to)
        if self.algAI == 'Highest move':
            return self.makeRandomBuild(_to)
        if self.algAI == 'Highest move and build':
            return self.makeBuildHighest(_to)
        if self.algAI == 'Heuristics 2143':
            return self.makeBuild2143(_to)

    def getAllCurrentAvailableMoves(self, verbose=False):
        pawn = self.player[0]
        moves = []
        for row in self.board:
            for col in self.board[row]:
                if self.board[row][col][1] is not None and self.board[row][col][1].startswith(pawn):
                    if verbose: print(f'Pawn on {(row, col)} can move to:')
                    dests = self.getAvailableMoves((row, col))
                    if verbose: print(dests)
                    moves += [((row, col), dest) for dest in dests]
        return moves

    def getAvailableMoves(self, _from):
        if not self.board[_from[0]][_from[1]][1]:
            warnings.warn('No pawn on this space')
            return False
        dests = []
        for row in self.board:
            for col in self.board[row]:
                if self.canMove(_from, (row, col), "ignore"):
                    dests.append((row, col))
        return dests

    def getAvailableBuilds(self, _to):
        dests = []
        for row in self.board:
            for col in self.board[row]:
                if self.canBuild((row, col), _to, filter="ignore"):
                    dests.append((row, col))
        return dests

    # Wipes board and sets pieces in default starting positions. Note that
    # Different starting positions can be achieved by replacing the indices in wipe().
    def wipe(self):
        self.board = setupBlankBoard()
        self.board['A'][1] = (self.board['B'][2][0], 'B1')
        self.board['B'][2] = (self.board['B'][2][0], 'R1')
        self.board['E'][1] = (self.board['B'][2][0], 'R2')
        self.board['E'][4] = (self.board['B'][2][0], 'B2')

    # Draws the current board state.
    # The numbers represent the building's state.
    # The letters represent the (B)lue and (R)ed pawns.
    def drawBoard(self):
        print('\t', end='')
        for i in range(5):
            print(f' {i + 1} \t', end='')
        print('\n', end='')
        for row in self.board:
            print(f'{row}\t', end='')
            for i in self.board[row]:
                el = self.board[row][i]
                if el[1] == None:
                    print(f' {el[0]} \t', end='')
                else:
                    print(f'{el[0]}{el[1]}\t', end='')
            print('\n', end='')

    # Check if any player has achieved victory.
    def isDone(self):
        for row in self.board:
            for col in self.board[row]:
                if self.board[row][col][0] == 3 and self.board[row][col][1]:
                    return True
        return False

    # Check if given space is occupied with a pawn.
    def spaceTaken(self, tuprc):
        if not self.board[tuprc[0]][tuprc[1]][1]: return False
        return True

    # Checks the difference in altitude (building height) between two spaces.
    # Note that number is positive if _to > _from, and negative otherwise.
    # Used when checking if move is viable.
    def getAltitudeDiff(self, _from, _to):
        altF = self.board[_from[0]][_from[1]][0]
        altT = self.board[_to[0]][_to[1]][0]
        return altT - altF

    # Checks if spaces are adjecent. Adjecency also counts for diagonals.
    # Used when checking if move is viable.

    def areAdjacent(self, A, B):
        if abs(ord(A[0]) - ord(B[0])) <= 1 and abs(A[1] - B[1]) <= 1 and A != B:
            return True
        return False

    def hasRoof(self, space):
        if self.board[space[0]][space[1]][0] == 4:
            return True
        return False

    def check_lets(self, let):
        if let not in ['A', 'B', 'C', 'D', 'E']:
            return False
        return True

    def check_nums(self, num):
        if 1 <= num <= 5:
            return True
        return False

    def canMove(self, _from, _to, filter="always"):
        warnings.simplefilter(filter)
        # takes from and to as tuprc.
        # check if spaces are adjacent:
        if not self.check_lets(_from[0]) or not self.check_lets(_to[0]):
            warnings.warn('Valid column indices are A-E.')
            return False
        if not self.check_nums(_from[1]) or not self.check_nums(_to[1]):
            warnings.warn('Valid row indices are 1-5.')
            return False
        if self.board[_from[0]][_from[1]][1] is None:
            warnings.warn('No pawn on specified space')
            return False
        elif not self.board[_from[0]][_from[1]][1].startswith(self.player[0]):
            warnings.warn('It is not this player\'s turn!')
            return False
        if not self.areAdjacent(_from, _to):
            warnings.warn(f'Spaces are not adjecent')
            return False
        # check if goal space is full
        if self.spaceTaken(_to):
            warnings.warn('target space already full')
            return False
        # check if the goal space is at most 1 higher than the start space
        if self.getAltitudeDiff(_from, _to) > 1:
            warnings.warn('Target space too high!')
            return False

        # check if goal space doesn't have dome:
        if self.hasRoof(_to):
            warnings.warn('Target space already has a roof')
            return False
        return True

    def build(self, space):
        if not self.spaceTaken(space) and not self.hasRoof(space):
            self.board[space[0]][space[1]] = (self.board[space[0]][space[1]][0] + 1, None)

    def canBuild(self, space, _to, filter='always'):
        warnings.simplefilter(filter)

        if not self.check_lets(space[0]) or not self.check_lets(_to[0]):
            warnings.warn('Valid column indices are A-E.')
            return False
        if not self.check_nums(int(space[1])) or not self.check_nums(int(_to[1])):
            warnings.warn('Valid row indices are 1-5.')
            return False
        if not self.areAdjacent(_to, space):
            warnings.warn('Can only build on a space, adjacent to the one just moved to.')
            return False
        if self.spaceTaken(space):
            warnings.warn('Can\'t build on occupied space.')
            return False
        if self.hasRoof(space):
            warnings.warn('Target space already has a roof')
            return False
        return True

    def move(self, _from, _to):
        color = self.board[_from[0]][_from[1]][1]
        if not self.canMove(_from, _to):
            raise Exception('Can\'t move here')
        self.board[_from[0]][_from[1]] = (self.board[_from[0]][_from[1]][0], None)
        self.board[_to[0]][_to[1]] = (self.board[_to[0]][_to[1]][0], color)

    def canRedMove(self):
        canMove = False
        for i in self.board.keys():
            for j in self.board[i].keys():
                if self.board[i][j][1] is not None and self.board[i][j][1].startswith("R"):
                    if self.getAvailableMoves((i, j)):
                        canMove = True
        return canMove

    def stateToHttpResponse(self):
        return HttpResponse(json.dumps(self.__dict__))

    def setAlgorithmAI(self, algorithm):
        self.algAI = algorithm
