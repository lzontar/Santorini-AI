import json

from django.http import HttpResponse

from .util.Santorini import Santorini
from .util.lib import mapperAlpha


def move(request):
    pos = request.GET

    _from = (mapperAlpha(pos['xOrig']), int(pos['yOrig']) + 1)
    _to = (mapperAlpha(pos['xTarget']), int(pos['yTarget']) + 1)
    move = game.move(_from, _to)

    gameDict = game.__dict__.copy()
    gameDict['availableConstructions'] = game.getAvailableBuilds(_to)

    return HttpResponse(json.dumps(gameDict))


def choose(request):
    pos = request.GET
    availableMoves = game.getAvailableMoves((mapperAlpha(pos['x']), int(pos['y']) + 1))

    return HttpResponse(json.dumps(availableMoves))


def build(request):
    pos = request.GET
    game.build((mapperAlpha(pos['x']), int(pos['y']) + 1))

    game.nextTurn()     # End turn
    # AI turn
    game.setPlayer()
    move = game.makeRandomMove()
    if not move:
        gameDict = game.__dict__.copy()
        gameDict['result'] = f'{game.player} loses!'
        gameDict['reason'] = f'{game.player} cannot move!'

        return HttpResponse(json.dumps(gameDict))

    build = game.makeRandomBuild(move[1])

    if game.isDone():
        gameDict = game.__dict__.copy()

        gameDict['result'] = f'{game.player} wins!'
        gameDict['reason'] = f'{game.player} reached the top floor!'

        return HttpResponse(json.dumps(gameDict))

    game.nextTurn()
    game.setPlayer()

    gameDict = game.__dict__.copy()
    gameDict['build'] = f'AI builds on {build}'
    gameDict['move'] = f'AI makes move {move[0]} -> {move[1]}'
    if game.isDone():
        gameDict['result'] = f'{game.player} wins!'
        gameDict['reason'] = f'{game.player} reached the top floor!'

    if not game.canRedMove():
        gameDict['result'] = f'{game.player} loses!'
        gameDict['reason'] = f'{game.player} cannot move!'

        return HttpResponse(json.dumps(gameDict))

    return HttpResponse(json.dumps(gameDict))


def init(request):
    global game
    game = Santorini()
    return game.stateToHttpResponse()
