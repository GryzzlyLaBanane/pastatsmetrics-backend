"""
Definition of views.
"""

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def pastats(request):
    return render(request, "main/research.html")


@csrf_exempt
def lobbydata_receiver(request):
    lobby_data = request.body.decode("utf-8")
    print(lobby_data)


def gamedata_receiver(request):
    gamedata = request.body.decode("utf-8")
    print(gamedata)