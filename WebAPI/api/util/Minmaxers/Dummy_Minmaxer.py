import sys
import os


from ..Santorini import Santorini, BIG_NUMBER, __MAXMINDICT__


def dummy_heuristic(state):
    """
    Dumb heuristic that evaluates standing as low as possible as a good board state

    """
    winning_state = BIG_NUMBER * __MAXMINDICT__[state.player]
    if state.isDone():
        return winning_state
    pawn_height_value = 0

    pawns = state.find_pawns()
    pawns = [space for l in list(pawns.values()) for space in l]
    for space in pawns:
        temp_value = 0
        let, num = space[0], space[1]
        height = state.board[let][num][0]
        temp_value -= height
        pawn = state.board[let][num][1]
        if pawn != state.player[0]:
            temp_value *= -1
        pawn_height_value += temp_value
    return pawn_height_value


class Dummy_Minmaxer(Santorini):

    def evaluate_current_board_state(self):
        self.algAI = 'Dummy'
        self.value = dummy_heuristic(self)

