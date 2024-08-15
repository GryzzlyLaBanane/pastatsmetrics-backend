from django import forms
from .models import (LobbyData, UnitsBuildingsCountMLA, GamesEconomyApm, KillsData, PlayersGamesHistory,
                     PlayerNameListData)


class SearchForm(forms.Form):
    player_name_id = forms.CharField(max_length=100)
    lobby_name_id = forms.CharField(max_length=100)

    def research(self, player_field, lobby_field):
        pass
