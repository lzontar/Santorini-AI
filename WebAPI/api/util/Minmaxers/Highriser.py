import sys
import os


from ..Santorini import Santorini, BIG_NUMBER, __MAXMINDICT__
import warnings


def pawn_height_proximity_value(state):
    """
    Heuristic function that evaluates game states.
    Favors situations where agent is standing as high as possible, surrounded
    by buildings that are as high as possible, while the oponnent is as low as possible.

    """
    winning_state = BIG_NUMBER * __MAXMINDICT__[state.player]
    if state.isDone():
        return winning_state
    pawn_height_value = 0

    pawns = state.find_pawns()
    for space in pawns.values():
        let, num = space[0], space[1]
        pawn = state.board[let][num][1]
        if not pawn: warnings.warn('There should be a pawn here.')  # should be redundant
        temp_value = 0
        temp_value += state.board[let][num][0]  # add the current height of the pawn
        for move in state.getAllCurrentAvailableMoves():
            if move[0] != space: continue  # this should be redundant
            dest = move[1]
            if not state.areAdjacent(space, dest): continue  # this should be redundant
            height = state.board[dest[0]][dest[1]][0]  # log the height of the adjecent space
            if height == 4: continue  # should be redundant
            if height == 3:  ## dodaj - ce si na 2. nadstropju
                if pawn == state.player[0]:
                    return winning_state  ## it is the current player's turn and an adjecent 3-space is open.
                else:
                    temp_value += height * 1.5  # the value should be high, since the opposing player could win next turn. However, this does not account for the possibility of simply building a roof there.
            elif height > 0:
                temp_value += height
            else:
                continue  # consider adding some reward here as well.
        if pawn != state.player[0]:
            temp_value *= -1
        pawn_height_value += temp_value
    return pawn_height_value

class Highriser(Santorini):

    def evaluate_current_board_state(self):
        self.algAI = 'Highriser'
        self.value = pawn_height_proximity_value(self)
