"""
Definition of views.
"""
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from .models import LobbyData


def pastats(request):
    return render(request, "main/research.html")


@csrf_exempt
def lobbydata_receiver(request):
    if request.method == 'POST':
        raw_lobby_data = request.body.decode("utf-8")
        lobby_data = json.loads(raw_lobby_data)
        new_lobby_to_save = LobbyData()
        new_lobby_to_save.check_n_save(lobby_data)
        print("turboteug", raw_lobby_data)
    return JsonResponse({'message': 'Data received'}, status=200)


@csrf_exempt
def gamedata_receiver(request):
    if request.method == 'POST':
        raw_game_data = request.body.decode("utf-8")
        print(raw_game_data)
    return JsonResponse({'message': 'Data received'}, status=200)