import seaborn as sns
from matplotlib import pyplot as plt
import pandas as pd
from santo import Santorini

AGENTS = ['Minmaxer', '2143', 'HighestMove', 'HighestMoveLowestBuild', 'Random']
def run_tests(white='Minmaxer', blue='2143', gpl=10, loops=5):
    s = Santorini()
    turns = []
    mode = [white, blue]
    games_per_loop = gpl
    loops = loops
    for j in range(loops):
        winners = {'Players' : ['White', 'Blue'], 'Wins' : [0,0]}
        for i in range(games_per_loop):
            player, turn = s.play(mode=mode)
            winners['Wins'][winners['Players'].index(player)]+=1
            turns.append(turn)
        winners = pd.DataFrame(winners)
        if j==0:
            all_winners = winners
        else:
            all_winners = all_winners.append(winners)


    fig, ax = plt.subplots(2,1)
    sns.barplot(x=list(all_winners.Wins), y=all_winners.Players, ax=ax[1])
    if not all(i==turns[0] for i in turns):
        sns.histplot(x=turns, ax=ax[0], binwidth=1)
    else: sns.histplot(x=turns, ax=ax[0])
    ax[0].set_title('Distribution of turn numbers')
    ax[1].set_title('Number of victories')
    plt.suptitle(f'{mode[0]} (W) vs. {mode[1]} (B)\n{loops}x{games_per_loop} games')
    plt.subplots_adjust(hspace=0.5, top=0.8)
    plt.savefig(f'./plots/{mode[0]}(w) vs {mode[1]}(b)-{loops}x{gpl} games')
    plt.show()


def ux_for_tests():
    white = input('Please input desired agent to play as white: ')
    if white not in AGENTS:
        print('Desired agent not available. Reverting to random.')
        white = 'Random'
    else:
        print(f'Selected {white}.')
    blue = input('Please input desired agent to play as blue: ')
    if blue not in AGENTS:
        print('Desired agent not available. Reverting to random.')
        blue = 'Random'
    else:
        print(f'Selected {blue}.')
    gpl = int(input('Please enter the desired number of games to play each loop: '))
    loops = int(input('Please enter number of loops to play (to show uncertainty): '))
    run_tests(white, blue, gpl, loops)

if __name__ == "__main__":
    ux_for_tests()