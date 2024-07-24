from django.urls import path
from . import views

app_name = "main"


urlpatterns = [
    path("", views.pastats, name="pastats"),
    path("api/lobbydata", views.lobbydata_receiver, name="lobbydata_receiver"),
    path("api/gamedata", views.gamedata_receiver, name="game_receiver"),
]
