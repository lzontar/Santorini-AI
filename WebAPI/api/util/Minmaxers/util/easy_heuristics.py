from ...Santorini import Santorini

###work in progress

def process_pawn_height(state, location, weight=1, exponent=1):
    return (weight*state.board[location[0]][location[1]][0])**exponent


def process_list_height(state, list_of_locations, weight=1, exponent=1):
    return sum([state.board[i[0]][i[1]][0] for i in list_of_locations])

