from django.urls import path
from . import views

app_name = "main"


urlpatterns = [
    path("", views.pastats, name="pastats"),
    path("api/lobbydata", views.lobbydata_receiver, name="lobbydata_receiver"),
    path("api/gamedata", views.gamedata_receiver, name="game_receiver"),
    path('api/search/', views.search_players, name='search_players'),
    path('charts=<str:lobby_id>', views.charts, name='charts'),
    path('api/get_charts', views.get_charts, name='get_charts'),
]
