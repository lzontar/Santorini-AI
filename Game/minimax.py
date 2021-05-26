from sys import maxsize #not using currently, should replace BIG_NUMBER

__MAXMINDICT__ = {'White' : 1, 'Blue' : -1}
BIG_NUMBER = 20000
#====== Heart of the MinMax algorithm. =====#
def MinMax(state, depth, start_depth, alpha, beta):
    player = state['State'].player
    sign = __MAXMINDICT__[player]
    if (depth==0) or (abs(state['State'].value) >= BIG_NUMBER) or state['State'].isDone(): #if victory is achieved in this state or we've reached our depth limit, do...
        return state, state
    goal = BIG_NUMBER * sign #this is the state value we want to achieve
    best_val = goal * -1 #start at the smallest possible value
    best_state = None
    parent, final_parent=None, None
    state['State'].make_children()
    for child in state['State'].children:
        observed_future, final_parent = MinMax(child, depth-1, start_depth, alpha, beta)
        observed_value = observed_future['State'].value # Extract the value, returned from the future state
        #print(observed_value)
        if abs(goal - observed_value) < abs(goal - best_val): #if this state gets us closer to our desired goal (victory), do...
            best_val = observed_value
            best_state = observed_future
            if depth == start_depth-1:
                parent = state

        ###===ALPHA BETA PRUNING
        if sign > 0:
            alpha = max(alpha,observed_value)
            if beta <= alpha:
                break
        else:
            beta = min(beta, observed_value)
            if beta <= alpha:
                break

    if depth!=start_depth: return best_state, parent
    else: return best_state, final_parent