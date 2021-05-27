
LETTERS = ['A', 'B', 'C', 'D', 'E']
NUMBERS = list(range(1,6))
players = ['Red', 'Blue']

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


def BlankPawnDict():
    return {'R' : [], 'B' : []}


def mapperAlpha(ix):
    mapper = {
        '0': 'A',
        '1': 'B',
        '2': 'C',
        '3': 'D',
        '4': 'E',
    }
    return mapper[ix]
