import datetime
import uuid
import json
from django.db import models
from django.utils import timezone


class PlayerNameListData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uber_id = models.CharField(max_length=50)  # Change to the real one
    player_name = models.CharField(max_length=100)
    date_name = models.CharField(max_length=100, null=True)

    class Meta:
        unique_together = (
            "uber_id",
            "player_name",
        )


class PlayersGamesHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lobby_id = models.CharField(max_length=100)
    uber_id = models.CharField(max_length=100)
    player_name = models.CharField(max_length=100, null=True)
    date_game = models.CharField(max_length=100, null=True)

    class Meta:
        unique_together = (
            "lobby_id",
            "uber_id",
        )


class KillsData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lobby_id = models.CharField(max_length=100)
    killer_name = models.CharField(max_length=100)
    defeated_name = models.CharField(max_length=100)
    time_kill = models.FloatField()

    class Meta:
        unique_together = (
            "lobby_id",
            "killer_name",
            "defeated_name",
        )


class LobbyData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lobby_id = models.CharField(max_length=100)
    uber_id = models.CharField(max_length=100)
    player_name = models.CharField(max_length=50)

    date_game = models.CharField(max_length=100, null=True)

    game_mode = models.CharField(max_length=100, null=True)
    game_name = models.CharField(max_length=200, default="None")
    # game_type = models.CharField(max_length=100, null=True)

    is_titan = models.BooleanField(null=True)
    is_ranked = models.BooleanField(null=True)
    system_name = models.CharField(max_length=200, null=True)
    planets_biomes = models.CharField(max_length=600, default="earth")

    winners = models.CharField(max_length=100, default="None")
    server_mods = models.CharField(max_length=1000, null=True)
    player_list = models.CharField(max_length=3000, null=True)
    player_count = models.IntegerField(default=0)

    user_name = models.CharField(max_length=50, null=True)
    is_Local = models.BooleanField(default=False)
    is_Public = models.BooleanField(default=False)
    is_FriendsOnly = models.BooleanField(default=False)
    is_Private = models.BooleanField(default=False)
    is_GalacticWar = models.BooleanField(default=False)
    is_LandAnywhere = models.BooleanField(default=False)
    is_ListenToSpectators = models.BooleanField(default=False)
    is_Sandbox = models.BooleanField(default=False)
    is_DynamicAlliances = models.BooleanField(default=False)
    dynamic_AllianceVictory = models.BooleanField(default=False)

    class Meta:
        unique_together = ("uber_id", "lobby_id", "player_name", "user_name")

