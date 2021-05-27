from ...Santorini import Santorini, getDist

###work in progress

def process_pawn_height(state, location, weight=1, exponent=1):
    return (weight*state.board[location[0]][location[1]][0])**exponent

def process_list_height(state, list_of_locations, weight=1):
    return sum([weight*state.board[i[0]][i[1]][0] for i in list_of_locations])

def process_list_height_no_roofs(state, list_of_locations, weight=1):
    final = 0
    for i in list_of_locations:
        height = state.board[i[0]][i[1]][0]
        if height != 4: final += weight*height
    return final

def process_list_altitude_diffs(state, location, list_of_locations, weight=1):
    return sum([weight*state.getAltitudeDiff(location, _to) for _to in list_of_locations])

def get_closest_enemy_pawn(state, this_space, weight=1, exponent=1):
    min = 10
    for space in state.find_pawns().values():
        pawn = state.board[space[0]][space[1]][1]
        if pawn[0] == state.player[0]: continue
        dist = getDist(space, this_space)
        if dist <min:
            min = dist
    return (weight*min)**exponent

def val_for_unattainable_state(state, val=100):
    for let in state.board:
        for num in state.board[let]:
            if state.board[let][num][0] == 3:
                for pawn in state.find_pawns().values():
                    if state.canMove(pawn, (let, num)) == 1: return val*20 #handler for winning state
                    else: return -val
    return 0