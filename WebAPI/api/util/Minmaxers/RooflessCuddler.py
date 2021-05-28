import sys
import os


from ..Santorini import Santorini, BIG_NUMBER, __MAXMINDICT__
from .util import easy_heuristics as heur
import warnings




def get_help2(state):
    """
    Heuristic function that evaluates game states.
    Favors situations where agent is standing as high as possible, surrounded
    by buildings that are as high as possible, while the oponnent is as low as possible.

    """

    winning_state = BIG_NUMBER * __MAXMINDICT__[state.player]
    if state.isDone():
        return winning_state
    val = 0
    pawns = state.find_pawns().values()
    for space in pawns:
        temp_value = 0
        #options =  state.getAvailableMoves(space)
        #pawn = state.board[space[0]][space[1]][1]
        #height = state.board[space[0]][space[1]][0]
        temp_value += heur.process_pawn_height(state, space, weight=5)
        #temp_value += heur.process_list_height(state, options)
        temp_value -= heur.get_closest_enemy_pawn(state, space, exponent=3)
        #temp_value += heur.val_for_unattainable_state(state)
        val += temp_value
    return val

class RooflessCuddler(Santorini):

    def evaluate_current_board_state(self):
        self.algAI = 'HelpInvoker'
        self.value = get_help2(self)

