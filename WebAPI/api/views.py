from django.shortcuts import render
from django.http import HttpResponse

import json

def index(request):
    return HttpResponse(json.dumps({
        'player1Pos': [[0, 1], [2, 2]],
        'player2Pos': [[2, 1], [3, 3]],
        'state': [
            [1, 1, 1, 0],
            [1, 1, 1, 0],
            [1, 1, 1, 0],
            [4, 1, 2, 3]
        ]
    }))
