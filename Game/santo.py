import warnings
import random
import copy
from sys import maxsize
warnings.simplefilter("always")

#The logic for the minimax algorithm is in a seperate file.
from minimax import MinMax, __MAXMINDICT__, BIG_NUMBER

"""
White is maximizer
Blue is minimizer
White always goes first. 
Starting Board states are determined at random.
"""

#=============Some helpful global variables, we should revert code to using these

LETTERS = ['A', 'B', 'C', 'D', 'E']
NUMBERS = list(range(1,6))
players = ['White', 'Blue']



#=== Some helper functions that help reset the board. ==#
def BlankPawnDict():
    return {'W' : [], 'B' : []}

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
    def __init__(self, new=True, board=None, turn=0):
        if new:
            ##Ensures that the board resets only if initializing new class
            ##(More santorini objects are initialized in the tree search for minmax)
            self.board = setupBlankBoard()
            self.pawns = BlankPawnDict()
            self.wipe()
        else:
            self.board = board
            self.pawns = self.get_pawns()
        self.cols = ['White', 'Blue']
        self.turn = turn
        self.player = self.cols[self.turn%2]
        self.value = 0 #Overriden by heuristic function, used in minmax.
        self.children = []
        self.evaluate_current_board_state() ## Function assigns heuristic value to current board state.
                                            ## See this function to see which heuristic is currently in use.



    #======================GAMEPLAY &  HELPERS=================================#
    # Only functions that are related to core Santorini gameplay,
    # Unrelated to any heuristics, tree search etc.

    ### Main game logic.
    def play(self, mode=None):

        """
        Main game logic. If 'Mode' is input,
        the players are predetermined (useful for running tests), otherwise, a
        simple terminal GUI is used to guide players through setup.

        Generally, the logic sets up the board, prompts the active player to move.
        Then, checks if the active player is winning (or can't build anywhere and losing),
        then prompts player to build.

        Finally, the active player is changed and this repeats.

        TODO:
        This function also includes a sort of ugly if-else tree to handle different
        AI / naive player logics. This should be migrated elsewhere
        """

        self.wipe()
        self.turn = 0
        print('WELCOME TO SANTORINI AI!')
        self.drawBoard()
        players = {}
        if not mode:
            mode = input('Please enter \'B\' to play as blue, \'W\' to play as white, '
                         '\'AI\' to watch AI play and \'WB\' to control both players! ')

            for i in mode:
                players.update({i.upper():'Human'})
            for i in ['W', 'B']:
                if i not in players:
                    players.update({i : input(f'Please enter agent for \'{i}\' (Random, HighestMove, HighestMoveBuild)')})
        else:
            for i in range(len(['W', 'B'])):
                players.update({['W', 'B'][i] : mode[i]})

        while(1):
            self.setPlayer()
            print(f"{self.player}'s turn!")
            if players[self.player[0]]=='Random':
                outcome = self.doAITurn(self.makeRandomMove, self.makeRandomBuild)
                if outcome != 1:
                    return self.process_outcome(outcome)
            elif players[self.player[0]]=='HighestMove':
                outcome = self.doAITurn(self.makeHighestMove, self.makeRandomBuild)
                if outcome != 1:
                    return self.process_outcome(outcome)
            elif players[self.player[0]]=='Minmaxer':
                outcome = self.minmaxer_turn()
                if outcome != 1:
                    return self.process_outcome(outcome)
            elif players[self.player[0]] == 'HighestMoveBuild':
                outcome = self.doAITurn(self.makeHighestMove, self.makeHighestBuild)
                if outcome != 1:
                    return self.process_outcome(outcome)
            elif players[self.player[0]] == 'HighestMoveLowestBuild':
                outcome = self.doAITurn(self.makeHighestMove, self.makeLowestBuild)
                if outcome != 1:
                    return self.process_outcome(outcome)
            elif players[self.player[0]] == '2143':
                outcome = self.doAITurn(self.makeHighestMove, self.Build2nd1st4th3rd)
                if outcome != 1:
                    return self.process_outcome(outcome)
            else:
                self.drawBoard()
                print(f'Please select {self.player} pawn to move (format = RC,RC ie. B2,B3)')
                moves = self.getAllCurrentAvailableMoves()
                if not moves:
                    print(f'No move available for {self.player}')
                    print(f'{self.player} loses!')
                    self.nextTurn()
                    self.setPlayer()
                    return self.player, self.turn - 1
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
                    return self.player, self.turn
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


    ### Main method for moving
    def build(self, space):
        """
        Is agnostic of the pawn position, so validation must be done before call.
        takes space as a (let, num) tuple.
        """
        if not self.spaceTaken(space) and not self.hasRoof(space):
            self.board[space[0]][space[1]] = (self.board[space[0]][space[1]][0]+1, None)

    ### Main method for moving
    def move(self, _from, _to):
        """
        takes _to and _from as a (let, num) tuple
        """
        color = self.board[_from[0]][_from[1]][1]
        if not self.canMove(_from, _to):
            self.drawBoard()
            print(_from, _to)
            raise Exception ('Can\'t move here')
        self.board[_from[0]][_from[1]] = (self.board[_from[0]][_from[1]][0], None)
        self.board[_to[0]][_to[1]] = (self.board[_to[0]][_to[1]][0], color)



    def wipe(self):
        ### Wipes board and sets pieces in default starting positions. Note that
        ### Different starting positions can be achieved by replacing the indices in wipe().
        ### Currently, random starting positions are implemented.
        self.board = setupBlankBoard()
        pawns = {'W' : [], 'B' : []}
        for i in range(2):
            for pawn in ['B', 'W']:
                num = random.choice([1, 2, 3, 4, 5])
                let = random.choice(['A', 'B', 'C', 'D', 'E'])
                while self.board[let][num][1]:
                    num = random.choice([1, 2, 3, 4, 5])
                    let = random.choice(['A', 'B', 'C', 'D', 'E'])
                self.board[let][num] = (0, pawn)
                pawns[pawn].append((let, num))
        self.pawns = pawns


    def drawBoard(self):
        """
        Draws the current board state. Used for the terminal UI
        ### The numbers represent the building's state.
        ### The letters represent the (B)lue and (W)hite pawns.
        """
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


    def isDone(self):
        ### Check if any player has achieved victory.
        ### Used as a stopping criterion in several functions.
        for row in self.board:
            for col in self.board[row]:
                if self.board[row][col][0] == 3 and self.board[row][col][1]:
                    return True
        return False

    def get_pawns(self):
        """
        ##returns the current location of pawns --
        used to save into self.pawns (which is not currently used)
        :return: dictionary of locations of pawns
        """
        nd = {'W' : [], 'B': []}
        for let in LETTERS:
            for num in NUMBERS:
                if self.board[let][num][1]:
                    nd[self.board[let][num][1]].append((let, num))
        return nd


    def setPlayer(self):
        """
        To be called to change the currently active player.
        This parameter is used for correct player move verification.
        """
        self.player = self.cols[self.turn%2]


    def doAITurn(self, move_function, build_function):
        """
        Simple shell function that handles generic AI turns for baseline players (ie random, 2431)

        Outcome 1 = not done
        Outcome 2 = win
        Outcome 3 = loss
        """
        move = move_function()
        if not move:
            return 2
        print(f'AI makes move {move[0]} -> {move[1]}')
        self.drawBoard()
        if self.isDone():
            return 3
        build = build_function(move[1])
        print(f'AI builds on {build}')
        self.drawBoard()
        return 1

    def process_outcome(self, outcome):
        """
        Handles outcomes, such as those output from doAITurn
            Outcome 2 = win
            Outcome 3 = loss
        """
        if outcome==2:
            print(f'No move available for {self.player}')
            print(f'{self.player} loses!')
            self.nextTurn()
            self.setPlayer()
            return self.player, self.turn - 1
        if outcome==3:
            print(f'{self.player} wins!')
            return self.player, self.turn

    def nextTurn(self):
        """
        Proceeds to the next turn.
        Parameter is used to determine which player can currently move (used in
        checking validity of selected moves).
        """
        self.turn += 1

    #======== MOVE VALIDATION AND VERIFICATION =====#
    # While the functions here are crutial to the gameplay loop, they
    # Should not cause any issues, since we have already implemented logic
    # that prevents us from makling illegal turns. Currently only used
    # for preventing errors by human players in the terminal and for
    # searching for valid moves by AI.


    def getAltitudeDiff(self, _from, _to):
        """
        Checks the difference in altitude (building height) between two spaces.
        Note that number is positive if _to > _from, and negative otherwise.
        Used when checking if move is viable.
        """

        altF = self.board[_from[0]][_from[1]][0]
        altT = self.board[_to[0]][_to[1]][0]
        return altT - altF

    def areAdjacent(self, A, B):
        ### Checks if spaces are adjecent. Adjecency also counts for diagonals.
        ### Used when checking if move is viable.
        if abs(ord(A[0]) - ord(B[0])) <= 1 and abs(A[1] - B[1]) <= 1 and A!=B:
            return True
        return False

    def hasRoof(self, space):
        if self.board[space[0]][space[1]][0] == 4:
            return True
        return False


    def check_lets(self, let):
        if let not in LETTERS:
            return False
        return True

    def check_nums(self, num):
        if num in NUMBERS:
            return True
        return False


    def spaceTaken(self, tuprc):
        ### Check if given space is occupied with a pawn.
        ### Used in move verification.
        if not self.board[tuprc[0]][tuprc[1]][1]: return False
        return True

    def canMove(self, _from, _to, filter="always"):
        """
        General method that uses several other validation methods to see if a proposed move is valid.
        filter should be set to "ignore" in automated functions to prevent warning spam on the console.
        Takes _to and _from as tuples of format (letter, number)
        """

        warnings.simplefilter(filter)

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

    def canBuild(self, space, _to, filter='always'):
        """
        Same as CanMove for building. See above.
        Space is the target space. To is the space from which one is building.
        """
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





    #=====================GENERAL AI METHODS========================#
    # This section contains some of the more important helper methods for all AI
    # (Naive players and heuristics) implementations. Get fammiliar with these first.

    def getAllCurrentAvailableMoves(self, verbose=False):
        """
        Gets all moves available to both pawns of the current player
        and outputs them in no particular order.
        """
        pawn = self.player[0]
        moves = []
        if not self.isDone():
            for row in self.board:
                for col in self.board[row]:
                    if self.board[row][col][1] == pawn:
                        if verbose: print(f'Pawn on {(row, col)} can move to:')
                        dests = self.getAvailableMoves((row, col))
                        if verbose:print(dests)
                        moves += [((row, col), dest) for dest in dests]
        return moves

    def getAvailableMoves(self, _from):
        """
        Returns all moves available for the pawn, located on the _from space
        :param _from:
        :return:
        """

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
        """
        Returns all moves available for the pawn, located on the _from space.
        This function assumes that the pawn has just legally moved to the space
        denoted as _to
        :return:
        """
        dests = []
        if not self.isDone():
            for row in self.board:
                for col in self.board[row]:
                    if self.canBuild((row, col), _to, filter="ignore"):
                        dests.append((row, col))
        return dests


    #======================NAIVE PLAYER METHODS=================================#
    # As baselines for our AI algorithms, we use naive rulesets.
    # The function doAITurn accepts a combination of a move and build function
    # to make decisions on quick random moves with no forward-look


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

    def makeHighestMove(self):
        options = self.getAllCurrentAvailableMoves()
        if not options:
            return False

        options.sort(key=lambda x: self.board[x[1][0]][x[1][1]], reverse=True)
        move = options[0]
        self.move(move[0], move[1])
        return move

    def makeHighestBuild(self, _to):
        options = self.getAvailableBuilds(_to)
        options.sort(key=lambda x: self.board[x[0]][x[1]][0], reverse=True)
        self.build(options[0])
        return options[0]



    def makeLowestBuild(self, _to):
        options = self.getAvailableBuilds(_to)
        options.sort(key=lambda x: self.board[x[0]][x[1]][0], reverse=False)
        self.build(options[0])
        return options[0]

    def Build2nd1st4th3rd(self, _to):
        ## This order ensures that this AI doesn't build the third floor
        ## for its oponnent (unless absolutely necessary)
        options = self.getAvailableBuilds(_to)
        for i in options:
            if self.board[i[0]][i[1]][0]==2:
                self.build(i)
                return i
        for i in options:
            if self.board[i[0]][i[1]][0]==1:
                self.build(i)
                return i

        for i in options:
            if self.board[i[0]][i[1]][0]==4:
                self.build(i)
                return i
        self.build(options[0])
        return options[0]


    ###===============MINIMAX ALGORITHM================#
    ## The core of the MinMax algorithm can be found in the minimax.py file.
    ## The function returns

    ## TODO: It's working quite slow, we should consider implementing alpha-beta pruning.

    def minmaxer_turn(self, depth=2):
        """

        This function is a standin for the doAITurn() function that handles the automatic gameplay of the AI (as said
        method is implemented for seperate move and build functions). The **DEPTH** parameter determines the size of tree
        search, passed to the Minimax algorithm in minmax.py.

        The strategy term is formatted as follows:
        {'State' : <instance_of_Santorini>, 'Move' : (_to, _from), 'Build': space},
        where the 'Move' and 'Build' parameters are the selected moves to be carried out this turn.

        Outcome 1 = not done
        Outcome 2 = win
        Outcome 3 = loss
        """
        _, strategy = MinMax({'State': self, 'Move' : ('Start', None), 'Build' : None}, depth, start_depth=depth, alpha=-maxsize, beta=maxsize)
        print(strategy)
        move = strategy['Move']
        if not move:
            return 2
        self.move(move[0], move[1])
        print(f'AI makes move {move[0]} -> {move[1]}')
        self.drawBoard()
        if self.isDone():
            return 3
        build = strategy['Build']
        self.build(build)
        print(f'AI builds on {build}')
        self.drawBoard()
        return 1

    def evaluate_current_board_state(self):
        """
        A general method that evaluates each board state upon Santorini() initialization.
        I suggest a good practice of changing the function call inside of here, instead of inside
        the Santorini initialization function.
        """
        self.value = self.pawn_height_proximity_value()

    def pawn_height_proximity_value(self):
        """
        Heuristic function that evaluates game states.
        Favors situations where agent is standing as high as possible, surrounded
        by buildings that are as high as possible, while the oponnent is as low as possible.

        """
        winning_state = BIG_NUMBER*__MAXMINDICT__[self.player]
        if self.isDone():
            return winning_state
        pawn_height_value = 0

        pawns = self.get_pawns()
        pawns = [space for list in list(pawns.values()) for space in list]
        for space in pawns:
            let, num = space[0], space[1]
            pawn = self.board[let][num][1]
            if not pawn: warnings.warn('There should be a pawn here.') # should be redundant
            temp_value = 0
            temp_value += self.board[let][num][0] #add the current height of the pawn
            for move in self.getAllCurrentAvailableMoves():
                if move[0] != space: continue #this should be redundant
                dest = move[1]
                if not self.areAdjacent(space, dest): continue #this should be redundant
                height = self.board[dest[0]][dest[1]][0] #log the height of the adjecent space
                if height == 4: continue # should be redundant
                if height == 3: ## dodaj - ce si na 2. nadstropju
                    if pawn == self.player[0]:
                        return winning_state ## it is the current player's turn and an adjecent 3-space is open.
                    else: temp_value += height*1.5 #the value should be high, since the opposing player could win next turn. However, this does not account for the possibility of simply building a roof there.
                elif height >0: temp_value += height
                else: continue # consider adding some reward here as well.
            if pawn != self.player[0]:
                temp_value *= -1
            pawn_height_value += temp_value
        return pawn_height_value

        #Used in minmax to create children of current board state.
    def make_children(self):
        self.children = self.get_all_next_states()

    def get_all_next_states(self): #used to generate list of children of current board state
        states = []
        if not self.isDone():
            for move in self.getAllCurrentAvailableMoves():
                s = Santorini(new=False, board=copy.deepcopy(self.board), turn=copy.deepcopy(self.turn))
                s.move(move[0], move[1])
                if not s.isDone():
                    for build in s.getAvailableBuilds(move[1]):
                        ss = Santorini(new=False, board=copy.deepcopy(s.board), turn=copy.deepcopy(s.turn))
                        ss.build(build)
                        ss.nextTurn()
                        ss.setPlayer()
                        assert ss.player != s.player
                        assert ss.turn == s.turn +1
                        states.append({'State' : ss, 'Move' : move, 'Build' : build})
                else:
                    states.append({'State' : s, 'Move' : move, 'Build' : None})
                    continue
            return states
        else: return [{'State' : self, 'Move' : ((None, None), (None, None)), 'Build' : None}]
