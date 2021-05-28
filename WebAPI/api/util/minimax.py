import time
from sys import maxsize  # not using currently, should replace BIG_NUMBER
import json

__MAXMINDICT__ = {'Red': 1, 'Blue': -1}
__MAXMINDICT__2 = {'Red': -1, 'Blue': 1}
BIG_NUMBER = 20000

MEMOIZATION = dict()


def emptyMemoization():
    global MEMOIZATION
    MEMOIZATION = dict()
    global ix
    ix = 0


ix = 0


def get_ix():
    global ix
    return ix

def MinMax(state, depth, start_depth, alpha, beta):
    #print('Inverse!')
    #if json.dumps(state_to_dict(state['State'])) in MEMOIZATION.keys():
    #    return MEMOIZATION[json.dumps(state_to_dict(state['State']))]
    if not state['State'].inverse: lib=__MAXMINDICT__
    else: lib=__MAXMINDICT__2
    player = state['State'].player
    sign = lib[player]
    goal = BIG_NUMBER * sign
    if (depth == 0) or (abs(state['State'].value) >= BIG_NUMBER) or state['State'].isDone():  # if victory is achieved in this state or we've reached our depth limit, do...
        return state['State'].value*sign, state

      # this is the state value we want to achieve
    best_val = goal * -1  # start at the smallest possible value
    best_state = None

    global ix
    ix += 1

    # time0 = time.time()
    state['State'].make_children()
    # time1 = time.time()
    # print(f'make_children executed in: {round(time1 - time0, 2)}s')

    for child in state['State'].children:
        _, observed_future = MinMax(child, depth - 1, start_depth, alpha, beta)
        if observed_future == None:continue
        observed_value = observed_future['State'].value  # Extract the value, returned from the future state
        if abs(goal - observed_value) < abs(
                goal - best_val):  # if this state gets us closer to our desired goal (victory), do...
            best_val = observed_value
            best_state = child

        ###===ALPHA BETA PRUNING
        if sign > 0:
            alpha = max(alpha, observed_value)
            if beta <= alpha:
                continue
        else:
            beta = min(beta, observed_value)
            if beta <= alpha:
                continue

    if json.dumps(state_to_dict(state['State'])) not in MEMOIZATION.keys():
        MEMOIZATION[json.dumps(state_to_dict(state['State']))] = best_state

    return best_val, best_state


def state_to_dict(_state):
    return {
        'board': _state.get_board(),
        'player': _state.get_player()
    }