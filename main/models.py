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
    player_color = models.CharField(max_length=100, null=True)

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
    player_name = models.CharField(max_length=50, null=True)

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

    def check_n_save(self, lobby_data):
        try :
            field_mapping = {
                "lobby_id": "lobby_id",
                "uber_id": "uber_id",
                "player_name": "player_name",
                "date_game": "the_date",
                "game_mode": "game_mode",
                "game_name": "game_name",
                "is_titan": "is_Titan",
                "is_ranked": "is_Ranked",
                "system_name": "system_name",
                "planets_biomes": "planets_biomes",
                "winners": "winners",
                "server_mods": "server_mods",
                "player_list": "player_list",
                "player_count": "player_count",
                "user_name": "user_name",
                "is_Local": "is_Local",
                "is_Public": "is_Public",
                "is_FriendsOnly": "is_FriendsOnly",
                "is_Private": "is_Hidden",
                "is_GalacticWar": "is_GalacticWar",
                "is_LandAnywhere": "is_LandAnywhere",
                "is_ListenToSpectators": "is_ListenToSpectators",
                "is_Sandbox": "is_Sandbox",
                "is_DynamicAlliances": "is_DynamicAlliances",
                "dynamic_AllianceVictory": "dynamic_AllianceVictory"
            }

            for field, key in field_mapping.items():
                if key in lobby_data:
                    setattr(self, field, lobby_data[key])

            # Handle defaults for fields that need them
            self.player_name = lobby_data.get("player_name", "None")
            self.game_name = lobby_data.get("game_name", "None")
            self.planets_biomes = lobby_data.get("planets_biomes", "earth")
            self.winners = lobby_data.get("winners", "None")
            self.server_mods = lobby_data.get("server_mods", "No server mods")
            self.player_count = lobby_data.get("player_count", 0)
            self.is_Local = lobby_data.get("is_Local", False)
            self.is_Public = lobby_data.get("is_Public", False)
            self.is_FriendsOnly = lobby_data.get("is_FriendsOnly", False)
            self.is_Private = lobby_data.get("is_Hidden", False)
            self.is_GalacticWar = lobby_data.get("is_GalacticWar", False)
            self.is_LandAnywhere = lobby_data.get("is_LandAnywhere", False)
            self.is_ListenToSpectators = lobby_data.get("is_ListenToSpectators", False)
            self.is_Sandbox = lobby_data.get("is_Sandbox", False)
            self.is_DynamicAlliances = lobby_data.get("is_DynamicAlliances", False)
            self.dynamic_AllianceVictory = lobby_data.get("dynamic_AllianceVictory", False)
            print("nickeld abant save")
            self.save()
            print("aftersave  heck bdd")
        except Exception as e:
            print("jsp frero mais y'a eu un pb", e)


class UnitsBuildingsCountMLA(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lobby_id = models.CharField(max_length=100)
    uber_id = models.CharField(max_length=100)
    current_time = models.FloatField()

    air_factory_count = models.IntegerField(default=0)
    advanced_air_factory_count = models.IntegerField(default=0)
    firefly_count = models.IntegerField(default=0)
    bumblebee_count = models.IntegerField(default=0)
    hornet_count = models.IntegerField(default=0)
    fabrication_aircraft_count = models.IntegerField(default=0)
    advanced_fabrication_aircraft_count = models.IntegerField(default=0)
    hummingbird_count = models.IntegerField(default=0)
    phoenix_count = models.IntegerField(default=0)
    kestrel_count = models.IntegerField(default=0)
    pelican_count = models.IntegerField(default=0)
    # commanders
    able_count = models.IntegerField(default=0)
    aceal_count = models.IntegerField(default=0)
    alpha_count = models.IntegerField(default=0)
    aryst0krat_count = models.IntegerField(default=0)
    chronoblip_count = models.IntegerField(default=0)
    delta_count = models.IntegerField(default=0)
    enzomatrix_count = models.IntegerField(default=0)
    fiveleafclover_count = models.IntegerField(default=0)
    fusion_count = models.IntegerField(default=0)
    gamma_count = models.IntegerField(default=0)
    gnugfur_count = models.IntegerField(default=0)
    invictus_count = models.IntegerField(default=0)
    jt100010117_count = models.IntegerField(default=0)
    kapowaz_count = models.IntegerField(default=0)
    kevin4001_count = models.IntegerField(default=0)
    mjon_count = models.IntegerField(default=0)
    mostlikely_count = models.IntegerField(default=0)
    nagasher_count = models.IntegerField(default=0)
    progenitor_count = models.IntegerField(default=0)
    sangudo_count = models.IntegerField(default=0)
    seniorhelix_count = models.IntegerField(default=0)
    stelarch_count = models.IntegerField(default=0)
    thechessknight_count = models.IntegerField(default=0)
    theta_count = models.IntegerField(default=0)
    toddfather_count = models.IntegerField(default=0)
    tykus24_count = models.IntegerField(default=0)
    vidicarus_count = models.IntegerField(default=0)
    visionik_count = models.IntegerField(default=0)
    ajax_count = models.IntegerField(default=0)
    armalisk_count = models.IntegerField(default=0)
    base_count = models.IntegerField(default=0)
    calyx_count = models.IntegerField(default=0)
    commandonut_count = models.IntegerField(default=0)
    gambitdfa_count = models.IntegerField(default=0)
    quad_locust_count = models.IntegerField(default=0)
    mobiousblack_count = models.IntegerField(default=0)
    osiris_count = models.IntegerField(default=0)
    potbelly79_count = models.IntegerField(default=0)
    pumpkin_count = models.IntegerField(default=0)
    raventhornn_count = models.IntegerField(default=0)
    sacrificiallamb_count = models.IntegerField(default=0)
    shadowdaemon_count = models.IntegerField(default=0)
    spartandano_count = models.IntegerField(default=0)
    spiderofmean_count = models.IntegerField(default=0)
    theflax_count = models.IntegerField(default=0)
    tokamaktech_count = models.IntegerField(default=0)
    twoboots_count = models.IntegerField(default=0)
    xenosentryprime_count = models.IntegerField(default=0)
    xinthar_count = models.IntegerField(default=0)
    zancrowe_count = models.IntegerField(default=0)
    beast_count = models.IntegerField(default=0)
    beast_count = models.IntegerField(default=0)
    beniesk_count = models.IntegerField(default=0)
    betadyne_count = models.IntegerField(default=0)
    centurion_count = models.IntegerField(default=0)
    damubbster_count = models.IntegerField(default=0)
    diremachine_count = models.IntegerField(default=0)
    enderstryke71_count = models.IntegerField(default=0)
    iwmiked_count = models.IntegerField(default=0)
    majuju_count = models.IntegerField(default=0)
    nefelpitou_count = models.IntegerField(default=0)
    nemicus_count = models.IntegerField(default=0)
    raizell_count = models.IntegerField(default=0)
    rallus_count = models.IntegerField(default=0)
    spz58624_count = models.IntegerField(default=0)
    stickman9000_count = models.IntegerField(default=0)
    unicorn_count = models.IntegerField(default=0)
    xov_count = models.IntegerField(default=0)
    zaazzaa_count = models.IntegerField(default=0)
    aeson_count = models.IntegerField(default=0)
    banditks_count = models.IntegerField(default=0)
    reaver_count = models.IntegerField(default=0)
    sadiga_count = models.IntegerField(default=0)
    # end coms
    spinner_count = models.IntegerField(default=0)
    galata_turret_count = models.IntegerField(default=0)
    flak_cannon_count = models.IntegerField(default=0)
    anti_nuke_launcher_count = models.IntegerField(default=0)
    holkins_count = models.IntegerField(default=0)
    pelter_count = models.IntegerField(default=0)
    dox_count = models.IntegerField(default=0)
    slammer_count = models.IntegerField(default=0)
    stinger_count = models.IntegerField(default=0)
    boom_count = models.IntegerField(default=0)
    bot_factory_count = models.IntegerField(default=0)
    advanced_bot_factory_count = models.IntegerField(default=0)
    grenadier_count = models.IntegerField(default=0)
    gil_e_count = models.IntegerField(default=0)
    bluehawk_count = models.IntegerField(default=0)
    catalyst_count = models.IntegerField(default=0)
    energy_plant_count = models.IntegerField(default=0)
    advanced_energy_plant_count = models.IntegerField(default=0)
    energy_storage_count = models.IntegerField(default=0)
    fabrication_bot_count = models.IntegerField(default=0)
    advanced_fabrication_bot_count = models.IntegerField(default=0)
    stitch_count = models.IntegerField(default=0)
    mend_count = models.IntegerField(default=0)
    fabrication_vehicle_count = models.IntegerField(default=0)
    advanced_fabrication_vehicle_count = models.IntegerField(default=0)
    wall_count = models.IntegerField(default=0)
    mine_count = models.IntegerField(default=0)
    skitter_count = models.IntegerField(default=0)
    laser_defense_tower_count = models.IntegerField(default=0)
    advanced_laser_defense_tower_count = models.IntegerField(default=0)
    single_laser_defense_tower_count = models.IntegerField(default=0)
    metal_extractor_count = models.IntegerField(default=0)
    advanced_metal_extractor_count = models.IntegerField(default=0)
    metal_storage_count = models.IntegerField(default=0)
    nuclear_missile_launcher_count = models.IntegerField(default=0)
    radar_count = models.IntegerField(default=0)
    advanced_radar_count = models.IntegerField(default=0)
    catapult_count = models.IntegerField(default=0)
    inferno_count = models.IntegerField(default=0)
    vanguard_count = models.IntegerField(default=0)
    sheller_count = models.IntegerField(default=0)
    leveler_count = models.IntegerField(default=0)
    ant_count = models.IntegerField(default=0)
    teleporter_count = models.IntegerField(default=0)
    unit_cannon_count = models.IntegerField(default=0)
    vehicle_factory_count = models.IntegerField(default=0)
    advanced_vehicle_factory_count = models.IntegerField(default=0)
    orbital_and_deepspace_radar_count = models.IntegerField(default=0)
    anchor_count = models.IntegerField(default=0)
    halley_count = models.IntegerField(default=0)
    umbrella_count = models.IntegerField(default=0)
    jig_count = models.IntegerField(default=0)
    orbital_fabrication_bot_count = models.IntegerField(default=0)
    orbital_factory_count = models.IntegerField(default=0)
    avenger_count = models.IntegerField(default=0)
    astraeus_count = models.IntegerField(default=0)
    sxx_1304_laser_platform_count = models.IntegerField(default=0)
    orbital_launcher_count = models.IntegerField(default=0)
    advanced_radar_satellite_count = models.IntegerField(default=0)
    arkyd_count = models.IntegerField(default=0)
    solar_array_count = models.IntegerField(default=0)
    barracuda_count = models.IntegerField(default=0)
    leviathan_count = models.IntegerField(default=0)
    orca_count = models.IntegerField(default=0)
    fabrication_ship_count = models.IntegerField(default=0)
    advanced_fabrication_ship_count = models.IntegerField(default=0)
    narwhal_count = models.IntegerField(default=0)
    stingray_count = models.IntegerField(default=0)
    naval_factory_count = models.IntegerField(default=0)
    advanced_naval_factory_count = models.IntegerField(default=0)
    kraken_count = models.IntegerField(default=0)
    piranha_count = models.IntegerField(default=0)
    torpedo_launcher_count = models.IntegerField(default=0)
    advanced_torpedo_launcher_count = models.IntegerField(default=0)
    wyrm_count = models.IntegerField(default=0)
    icarus_count = models.IntegerField(default=0)
    horsefly_count = models.IntegerField(default=0)
    angel_count = models.IntegerField(default=0)
    zeus_count = models.IntegerField(default=0)
    lob_count = models.IntegerField(default=0)
    stryker_count = models.IntegerField(default=0)
    locust_count = models.IntegerField(default=0)
    colonel_count = models.IntegerField(default=0)
    spark_count = models.IntegerField(default=0)
    storm_count = models.IntegerField(default=0)
    drifter_count = models.IntegerField(default=0)
    manhattan_count = models.IntegerField(default=0)
    atlas_count = models.IntegerField(default=0)
    ragnarok_count = models.IntegerField(default=0)
    ares_count = models.IntegerField(default=0)
    omega_count = models.IntegerField(default=0)
    hermes_count = models.IntegerField(default=0)
    artemis_count = models.IntegerField(default=0)
    helios_count = models.IntegerField(default=0)
    typhoon_count = models.IntegerField(default=0)
    squall_count = models.IntegerField(default=0)
    barnacle_count = models.IntegerField(default=0)
    kaiju_count = models.IntegerField(default=0)
    avatar_count = models.IntegerField(default=0)


# class UnitsBuildingsCountLegion(models.Model):
# class UnitsBuildingsCountSecondWave(models.Model):
# class UnitsBuildingsCountThorosmen(models.Model):
# class UnitsBuildingsCountS17andOthers(models.Model):


class GamesEconomyApm(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lobby_id = models.CharField(max_length=100)
    uber_id = models.CharField(max_length=100)

    apm_data = models.FloatField(default=0)
    current_time = models.FloatField()

    energy_gain = models.FloatField()
    energy_loss = models.FloatField()
    energy_net = models.FloatField()
    energy_efficiency_perc = models.FloatField()
    energy_current_energy = models.FloatField()
    energy_max_energy = models.FloatField()

    metal_gain = models.FloatField()
    metal_loss = models.FloatField()
    metal_net = models.FloatField()
    metal_efficiency_perc = models.FloatField()
    metal_current_metal = models.FloatField()
    metal_max_metal = models.FloatField()
    metal_win_rate = models.FloatField()
    metal_loss_rate = models.FloatField()

    metal_wasted = models.FloatField(default=0)
    metal_produced = models.FloatField(default=0)
    energy_wasted = models.FloatField(default=0)
    energy_produced = models.FloatField(default=0)
    efficiency = models.FloatField(default=0)
