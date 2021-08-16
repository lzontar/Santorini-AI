import sys
import os


from ..Santorini import Santorini, BIG_NUMBER, __MAXMINDICT__, __MAXMINDICT__2
from .util import easy_heuristics as heur
import warnings




def get_help(state):
    """
    Heuristic function that evaluates game states.
    Favors situations where agent is standing as high as possible, surrounded
    by buildings that are as high as possible, while the oponnent is as low as possible.

    """
    if not state.inverse:
        lib = __MAXMINDICT__
    else: lib = __MAXMINDICT__2
    winning_state = BIG_NUMBER * lib[state.player]
    if state.isDone():
        return winning_state
    val = 0
    pawns = state.find_pawns().values()
    for space in pawns:
        temp_value = 0
        options =  state.getAvailableMoves(space)
        pawn = state.board[space[0]][space[1]][1]
        height = state.board[space[0]][space[1]][0]
        if height>2:print(f'{pawn} observes possibility of moving to {height}')
        if height == 3:
            print('ObservingPossibilityOfThree')
            temp_value = winning_state
            print(f'{pawn[0] == state.player[0]}' )
            if pawn[0] != state.player[0]:
                temp_value *= -0.9
            val+= temp_value
            continue
        #temp_value += heur.process_pawn_height(state, space, weight=3)
        temp_value += heur.process_list_height(state, options)
        temp_value += heur.get_closest_enemy_pawn(state, space, exponent=2)
        temp_value += heur.val_for_unattainable_state(state)
        if pawn[0] != state.player[0]:
            temp_value *= -0.9
        val += temp_value
    return val

class SansInvoker1(Santorini):

    def evaluate_current_board_state(self):
        self.algAI = 'SansInvoker1'
        self.value = get_help(self)
