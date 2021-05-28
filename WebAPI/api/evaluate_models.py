import seaborn as sns
from matplotlib import pyplot as plt
import pandas as pd
plt.style.use('bmh')
import os
print(os.getcwd())
from util.Santorini import Santorini
from pytictoc import TicToc
from pathlib import Path


from util.minmaxer_names import ALL_MINMAXERS
from util.ObjectInstanceDictionary import INSTANCES
AGENTS = ['3214', 'HighestMove', 'HighestMoveLowestBuild', 'Random', 'RandomMinmaxer'] + ALL_MINMAXERS

def run_tests(white='Minmaxer', blue='3214', gpl=10, loops=5, depth=2):

    turns = []
    mode1 = [white, blue]
    mode2 = [blue, white]
    games_per_loop = gpl
    loops = loops
    folder = f'{mode1[0]} vs {mode1[1]} d={depth}'
    #for mode in [mode1, mode2]:
    for mode in [mode1, mode2]:

        need_casting = any([i in ALL_MINMAXERS for i in mode])
        for j in range(loops):
            winners = {'Players' : ['Red', 'Blue'], 'Wins' : [0,0]}
            for i in range(games_per_loop):
                print(f'****************GAME {i}*************')
                s = Santorini(True)
                players = s.make_players(mode)
                print(players)
                while not s.isDone() and not s.amDead():
                    turn = s.turn
                    print(turn)
                    if turn%2==0:inverse=True
                    else: inverse=False
                    player = players[s.cols[turn%2][0]]
                    if need_casting:
                        print(type(s).__name__)
                        print(player)
                        if player not in INSTANCES:
                            obj = Santorini(inverse)
                        else: obj = INSTANCES[player]
                        s = obj.BoardState(inverse, new=False, board=s.board, turn = s.turn)
                    s.play_turn(players)
                player = s.player
                turn = s.turn
                winners['Wins'][winners['Players'].index(player)]+=1
                turns.append(turn)
            winners = pd.DataFrame(winners)
            if j==0:
                all_winners = winners
            else:
                all_winners = all_winners.append(winners)


        fig, ax = plt.subplots(2,1)
        sns.barplot(x=list(all_winners.Wins), y=all_winners.Players, ax=ax[1], palette=['red', 'blue'])
        if not all(i==turns[0] for i in turns):
            sns.kdeplot(x=turns, ax=ax[0])
        else: sns.histplot(x=turns, ax=ax[0])
        ax[0].set_title('Distribution of turn numbers')
        ax[1].set_title('Number of victories')
        plt.suptitle(f'{mode[0]} (R) vs. {mode[1]} (B)\n{loops}x{games_per_loop} games')
        plt.subplots_adjust(hspace=0.5, top=0.8)
        Path(f"./plots/{folder}").mkdir(parents=True, exist_ok=True)
        plt.savefig(f'./plots/{folder}/{mode[0]}(w) vs {mode[1]}(b)-{loops}x{gpl} games', bbox_inches='tight')
        plt.show()


def ux_for_tests(agent, depth):
    red = agent # input('Please input desired agent to play as white: ')
    if red not in AGENTS:
        print('Desired agent not available. Reverting to random.')
        red = 'Random'
    else:
        print(f'Selected {red}.')
    blue = agent # input('Please input desired agent to play as blue: ')
    if blue not in AGENTS:
        print('Desired agent not available. Reverting to random.')
        blue = 'Random'
    else:
        print(f'Selected {blue}.')
    gpl = 10 # int(input('Please enter the desired number of games to play each loop: '))
    loops = 2 # int(input('Please enter number of loops to play (to show uncertainty): '))
    run_tests(red, blue, gpl, loops, depth)

if __name__ == "__main__":
    ux_for_tests()