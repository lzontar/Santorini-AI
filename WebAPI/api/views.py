import json

from django.http import HttpResponse

from .util.Santorini import Santorini
from .util.Minmaxers.LowIsGood import LowIsGood
from .util.Minmaxers.Highriser import Highriser
from .util.Minmaxers.Highriser2 import Highriser2
from .util.lib import mapperAlpha


def move(request):
    pos = request.GET

    _from = (mapperAlpha(pos['xOrig']), int(pos['yOrig']) + 1)
    _to = (mapperAlpha(pos['xTarget']), int(pos['yTarget']) + 1)
    move = game.move(_from, _to)

    gameDict = game.__dict__.copy()
    gameDict['availableConstructions'] = game.getAvailableBuilds(_to)

    if game.isDone():
        return win()

    gameDict['children'] = []
    return HttpResponse(json.dumps(gameDict))


def choose(request):
    pos = request.GET
    availableMoves = game.getAvailableMoves((mapperAlpha(pos['x']), int(pos['y']) + 1))

    return HttpResponse(json.dumps(availableMoves))


def win():
    gameDict = game.__dict__.copy()
    gameDict['result'] = f'{game.player} wins!'
    gameDict['reason'] = f'{game.player} reached the top floor!'
    gameDict['winner'] = game.player.lower()
    gameDict['children'] = []
    return HttpResponse(json.dumps(gameDict))

def build(request):
    pos = request.GET
    game.build((mapperAlpha(pos['x']), int(pos['y']) + 1))

    game.nextTurn()  # End turn
    if game.isDone():
        return win()

    game.play(mode=[None, game.algAI], cmd=False)

    if game.isDone():
        return win()

    game.setPlayer()

    gameDict = game.__dict__.copy()
    gameDict['children'] = []
    return HttpResponse(json.dumps(gameDict))

def get_game(alg):
    if alg == 'LowIsGood':
        return LowIsGood()
    elif alg == 'Highriser':
        return Highriser()
    elif alg == 'Highriser2':
        return Highriser2()
    return Santorini()

def init(request):
    algorithm = request.GET['alg']

    global game
    game = get_game(algorithm)
    game.setAlgorithmAI(algorithm)

    return game.stateToHttpResponse()


# AI turn
    # game.setPlayer()
    # move = game.makeRandomMove()
    # if not move:
    #     gameDict = game.__dict__.copy()
    #     gameDict['result'] = f'{game.player} loses!'
    #     gameDict['reason'] = f'{game.player} cannot move!'
    #     gameDict['winner'] = game.cols[(game.turn + 1) % 2].lower()
    #
    #     return HttpResponse(json.dumps(gameDict))
    #
    # build = game.makeRandomBuild(move[1])
    #
    # if game.isDone():
    #     gameDict = game.__dict__.copy()
    #
    #     gameDict['result'] = f'{game.player} wins!'
    #     gameDict['reason'] = f'{game.player} reached the top floor!'
    #     gameDict['winner'] = game.player.lower()
    #
    #     return HttpResponse(json.dumps(gameDict))
    #
    # game.nextTurn()
    # game.setPlayer()
    #
    # gameDict = game.__dict__.copy()
    # gameDict['build'] = f'AI builds on {build}'
    # gameDict['move'] = f'AI makes move {move[0]} -> {move[1]}'
    # if game.isDone():
    #     gameDict['result'] = f'{game.player} wins!'
    #     gameDict['reason'] = f'{game.player} reached the top floor!'
    #     gameDict['winner'] = game.player.lower()
    #
    # if not game.canRedMove():
    #     gameDict['result'] = f'{game.player} loses!'
    #     gameDict['reason'] = f'{game.player} cannot move!'
    #     gameDict['winner'] = game.cols[(game.turn + 1) % 2].lower()
    #
    #     return HttpResponse(json.dumps(gameDict))