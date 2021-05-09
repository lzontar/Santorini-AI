import warnings
import random
warnings.simplefilter("always")


### Clears the board of all buildings and pieces.
def setupBlankBoard():
    empty_space = (0, None)
    board = {}
    row = {}
    for i in range(1, 6):
        row.update({i : empty_space})
    for letter in ['A', 'B', 'C', 'D', 'E']:
        board.update({letter : row.copy()})
    return board



class Santorini():
    def __init__(self):
        self.board = setupBlankBoard()
        self.wipe()
        self.cols = ['White', 'Blue']
        self.turn = 0
        self.player = self.cols[self.turn%2]


    ### To be called to change the currently active player.
    ### This parameter is used for correct player move verification.
    def setPlayer(self):
        self.player = self.cols[self.turn%2]


    ### Proceeds to the next turn. Parameter is used to determine which player
    ### can move.
    def nextTurn(self):
        self.turn += 1



    def makeRandomMove(self):
        options = self.getAllCurrentAvailableMoves()
        move = random.choice(options)
        self.move(move[0], move[1])
        return move

    def makeRandomBuild(self, _to):
        options = self.getAvailableBuilds(_to)
        b = random.choice(options)
        self.build(b)
        return b
    ### Main game logic.
    ### Clears board, prompts first player to move.
    ### Checks if player is winning, if not, prompts player to build,
    ### Then changes active player and repeats.
    def play(self):
        self.wipe()
        self.turn = 0
        print('WELCOME TO SANTORINI AI!')
        self.drawBoard()
        players = {}
        mode = input('Please enter \'B\' to play as blue, \'W\' to play as white, \'AI\' to watch AI play and \'WB\' to control both players! ')

        for i in mode:
            players.update({i.upper():'Human'})
        for i in ['W', 'B']:
            if i not in players:
                players.update({i : 'AI'})

        while(1):
            self.setPlayer()
            if players[self.player[0]]=='AI':
                move = self.makeRandomMove()
                print(f'AI makes move {move[0]} -> {move[1]}')
                self.drawBoard()
                if self.isDone():
                    print(f'{self.player} wins!')
                    break
                build = self.makeRandomBuild(move[1])
                print(f'AI builds on {build}')
                self.drawBoard()
            else:
                print(f"{self.player}'s turn!")
                self.drawBoard()
                print(f'Please select {self.player} pawn to move (format = RC,RC ie. B2,B3)')
                self.getAllCurrentAvailableMoves()
                tup = input().split(',')
                while len(tup) != 2:
                    print('Incorrect format! Please enter START_SPACE,END_SPACE, separated with a comma!')
                    tup = input().split(',')
                _from = (tup[0][0].upper(), int(tup[0][1]))
                _to = (tup[1][-2].upper(), int(tup[1][-1]))
                while not self.canMove(_from, _to):
                    print('Invalid move!')
                    print(f'Please select {self.player} pawn to move (format = RC,RC ie. B2,B3)')
                    tup = input().split(',')
                    _from = (tup[0][0].upper(), int(tup[0][1]))
                    _to = (tup[1][-2].upper(), int(tup[1][-1]))
                self.move(_from, _to)
                if self.isDone():
                    print(f'{self.player} wins!')
                    break
                self.drawBoard()
                print(f'Please select a space adjecent to {_to} to build on!')
                print(f'Available build destinations: {self.getAvailableBuilds(_to)}')
                tup = input()
                b = (tup[0].upper(), int(tup[1]))
                while not self.canBuild(b, _to):
                    print('Can\'t build on desired space!')
                    print(f'Please select a space adjecent to {_to} to build on!')
                    tup = input()
                    b = (tup[0].upper(), int(tup[1]))
                self.build(b)
            self.nextTurn()



    def getAllCurrentAvailableMoves(self, verbose=False):
        pawn = self.player[0]
        moves = []
        for row in self.board:
            for col in self.board[row]:
                if self.board[row][col][1] == pawn:
                    if verbose: print(f'Pawn on {(row, col)} can move to:')
                    dests = self.getAvailableMoves((row, col))
                    if verbose:print(dests)
                    moves += [((row, col), dest) for dest in dests]
        return moves

    def getAvailableMoves(self, _from):
        if not self.board[_from[0]][_from[1]][1]:
            warnings.warn('No pawn on this space')
            return False
        dests = []
        for row in self.board:
            for col in self.board[row]:
                if self.canMove(_from, (row,col), "ignore"):
                    dests.append((row, col))
        return dests

    def getAvailableBuilds(self, _to):
        dests = []
        for row in self.board:
            for col in self.board[row]:
                if self.canBuild((row, col), _to, filter="ignore"):
                    dests.append((row, col))
        return dests


    ### Wipes board and sets pieces in default starting positions. Note that
    ### Different starting positions can be achieved by replacing the indices in wipe().
    def wipe(self):
        self.board = setupBlankBoard()
        self.board['B'][2] = (self.board['B'][2][0], 'B')
        self.board['B'][4] = (self.board['B'][2][0], 'W')
        self.board['D'][2] = (self.board['B'][2][0], 'W')
        self.board['D'][4] = (self.board['B'][2][0], 'B')


    ### Draws the current board state.
    ### The numbers represent the building's state.
    ### The letters represent the (B)lue and (W)hite pawns.
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


    ### Check if any player has achieved victory.
    def isDone(self):
        for row in self.board:
            for space in row:
                if space[0] == 3 and space[1]:
                    return True
        return False

    ### Check if given space is occupied with a pawn.
    def spaceTaken(self, tuprc):
        if not self.board[tuprc[0]][tuprc[1]][1]: return False
        return True

    ### Checks the difference in altitude (building height) between two spaces.
    ### Note that number is positive if _to > _from, and negative otherwise.
    ### Used when checking if move is viable.
    def getAltitudeDiff(self, _from, _to):
        altF = self.board[_from[0]][_from[1]][0]
        altT = self.board[_to[0]][_to[1]][0]
        return altT - altF


    ### Checks if spaces are adjecent. Adjecency also counts for diagonals.
    ### Used when checking if move is viable.

    def areAdjacent(self, A, B):
        if abs(ord(A[0]) - ord(B[0])) <= 1 and abs(A[1] - B[1]) <= 1 and A!=B:
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
        ##takes from and to as tuprc.
        ##check if spaces are adjacent:
        if not self.check_lets(_from[0]) or not self.check_lets(_to[0]):
            warnings.warn('Valid column indices are A-E.')
            return False
        if not self.check_nums(_from[1]) or not self.check_nums(_to[1]):
            warnings.warn('Valid row indices are 1-5.')
            return False
        if self.board[_from[0]][_from[1]][1] is None:
            warnings.warn('No pawn on specified space')
            return False
        elif self.board[_from[0]][_from[1]][1] != self.player[0]:
            warnings.warn('It is not this player\'s turn!')
            return False
        if not self.areAdjacent(_from, _to):
            warnings.warn(f'Spaces are not adjecent')
            return False
        ##check if goal space is full
        if self.spaceTaken(_to):
            warnings.warn('target space already full')
            return False
        ##check if the goal space is at most 1 higher than the start space
        if self.getAltitudeDiff(_from, _to) > 1:
            warnings.warn('Target space too high!')
            return False

        ##check if goal space doesn't have dome:
        if self.hasRoof(_to):
            warnings.warn('Target space already has a roof')
            return False
        return True

    def build(self, space):
        if not self.spaceTaken(space) and not self.hasRoof(space):
            self.board[space[0]][space[1]] = (self.board[space[0]][space[1]][0]+1, None)

    def canBuild(self, space, _to, filter='always'):
        warnings.simplefilter(filter)

        if not self.check_lets(space[0]) or not self.check_lets(_to[0]):
            warnings.warn('Valid column indices are A-E.')
            return False
        if not self.check_nums(int(space[1])) or not self.check_nums(int(_to[1])):
            warnings.warn('Valid row indices are 1-5.')
            return False
        if not self.areAdjacent(_to, space):
            warnings.warn('Can only build on a space, adjecent to the one just moved to.')
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
            raise Exception ('Can\'t move here')
        self.board[_from[0]][_from[1]] = (self.board[_from[0]][_from[1]][0], None)
        self.board[_to[0]][_to[1]] = (self.board[_to[0]][_to[1]][0], color)


s = Santorini()
s.play()