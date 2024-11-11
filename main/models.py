import datetime
import uuid
import json
from django.db import models
from django.utils import timezone
from django.db.models import Sum

class PlayerNameListData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uber_id = models.CharField(max_length=50)  # Change to the real one
    player_name = models.CharField(max_length=100)
    date_name = models.CharField(max_length=100, null=True)

    def check_n_save(self, puber_id, pplayer_name, pdate):
        self.uber_id = puber_id
        self.player_name = pplayer_name
        self.date_name = pdate

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
    date_game_start = models.CharField(max_length=100, null=True)
    date_game_last = models.CharField(max_length=100, null=True)
    player_color = models.CharField(max_length=100, null=True)

    def check_n_save(self, plobby_id, puber_id, pplayer_name):
        if not PlayersGamesHistory.objects.filter(lobby_id=plobby_id, uber_id=puber_id).exists():
            self.uber_id = puber_id
            self.lobby_id = plobby_id
            self.player_name = pplayer_name

            lobby_data = LobbyData.objects.get(lobby_id=plobby_id, uber_id=puber_id)
            self.date_game_start = lobby_data.date_game_start
            self.date_game_last = lobby_data.date_game_last
            print("bah oui fils de pute", lobby_data.player_list,lobby_data.player_list[lobby_data.player_name][1])
            self.player_color = json.loads(lobby_data.player_list)[lobby_data.player_name][1]

            self.save()

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

    def check_n_save(self, kill_data, lobby_id, current_time):
        self.lobby_id = lobby_id

        if len(kill_data) != 0:
            try:
                kill_data = json.loads(kill_data)

                self.defeated_name = kill_data["defeated"]["name"]
                self.killer_name = kill_data["killer"]["name"]
                self.time_kill = int(current_time)
                self.save()
            except Exception:
                pass
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

    date_game_start = models.CharField(max_length=100, null=True)
    date_game_last = models.CharField(max_length=100, null=True)

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
        if LobbyData.objects.filter(lobby_id=lobby_data['lobby_id']).exists():
            print("An entry with this lobby_id already exists. Skipping save.")
            return
        else:
            try :
                field_mapping = {
                    "lobby_id": "lobby_id",
                    "uber_id": "uber_id",
                    "player_name": "player_name",
                    "date_game_start": "the_date",
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

    def update_lobby_data(self, lobby_data):
        try:
            field_mapping = {
                "lobby_id": "lobby_id",
                "uber_id": "uber_id",
                "player_name": "player_name",
                "date_game_last": "the_date",
                "game_mode": "game_type",
                "is_ranked": "is_ladder1v1",
                "system_name": "system_name",
                "winners": "game_victors",
                "user_name": "user_name",
                "is_LandAnywhere": "is_land_anywhere",
                "is_ListenToSpectators": "is_listen_to_spectators",
                "is_Sandbox": "is_sandbox",
                "is_DynamicAlliances": "is_dynamic_alliances",
                "dynamic_AllianceVictory": "dynamic_alliance_victory",
                "is_GalacticWar": "is_galacticwar",
            }

            # Update fields if they exist in the incoming data
            for field, key in field_mapping.items():
                if key in lobby_data:
                    setattr(self, field, lobby_data[key])

            # Handle defaults for fields that need them, only if the field is not provided in the data
            if "player_name" not in lobby_data:
                self.player_name = "None"
            if "game_victors" not in lobby_data:
                self.winners = "None"
            if "is_galacticwar" not in lobby_data:
                self.is_GalacticWar = False
            if "is_land_anywhere" not in lobby_data:
                self.is_LandAnywhere = False
            if "is_listen_to_spectators" not in lobby_data:
                self.is_ListenToSpectators = False
            if "is_sandbox" not in lobby_data:
                self.is_Sandbox = False
            if "is_dynamic_alliances" not in lobby_data:
                self.is_DynamicAlliances = False
            if "dynamic_alliance_victory" not in lobby_data:
                self.dynamic_AllianceVictory = False
            # Handle player_list
            if "player_list" in lobby_data:
                print("IN GAME LOBBYDATA", lobby_data)


                # en gros ici on a
                #  existing_player_list = self.player_list = {'< blank > (88)': '4722181537817857297', 'Malgour': '17851776222802156084'}
                # et lobby_data["player_list"] = [['Malgour', [223, 175, 0]], ['< blank > (88)', [223, 223, 0]]
                existing_player_list = self.player_list
                result = {}
                for player_name, colors in lobby_data["player_list"]:
                    if player_name in existing_player_list:
                        # Get the ID from existing_player_list
                        player_id = existing_player_list[player_name]
                        # Add to result in the required format
                        result[player_name] = [player_id, colors]
                print("BAH OU IRESULT", result)
                self.player_list = result

                # new_player_data = lobby_data["player_list"]
                # self.player_count = len(new_player_data)
                #
                #
                # if existing_player_list:
                #     try:
                #         existing_player_list = json.loads(existing_player_list.replace("'", "\""))
                #     except json.JSONDecodeError:
                #         existing_player_list = {}
                #
                # if not isinstance(existing_player_list, dict):
                #     existing_player_list = {}
                #
                # for player_info in new_player_data:
                #     player_name = player_info[0]
                #     player_stats = player_info[1]
                #
                #     if player_name in existing_player_list:
                #         if isinstance(existing_player_list[player_name], list) and player_stats not in \
                #                 existing_player_list[player_name]:
                #             existing_player_list[player_name].append(player_stats)
                #         elif not isinstance(existing_player_list[player_name], list):
                #             if isinstance(existing_player_list[player_name], str) or isinstance(
                #                     existing_player_list[player_name], int):
                #                 existing_player_list[player_name] = [existing_player_list[player_name]]
                #             if player_stats not in existing_player_list[player_name]:
                #                 existing_player_list[player_name].append(player_stats)
                #     else:
                #         existing_player_list[player_name] = player_stats
                #
                # self.player_list = json.dumps(existing_player_list, ensure_ascii=False)
            else:
                self.player_count = 0
            self.save()
        except Exception as e:
            print("An error occurred while updating the lobby data:", e)


class UnitsBuildingsCountMLA(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lobby_id = models.CharField(max_length=100)
    uber_id = models.CharField(max_length=100)
    current_time = models.IntegerField()

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
    radar_jamming_station_count = models.IntegerField(default=0)

    def check_n_save(self, lobby_id, uber_id, time_data, unb_data):
        self.lobby_id = lobby_id
        self.uber_id = uber_id
        self.current_time = int(time_data)
        full_list_unb = {
            "/pa/units/air/air_factory/air_factory.json": "air_factory_count",
            "/pa/units/air/air_factory_adv/air_factory_adv.json": "advanced_air_factory_count",
            "/pa/units/air/air_scout/air_scout.json": "firefly_count",
            "/pa/units/air/bomber/bomber.json": "bumblebee_count",
            "/pa/units/air/bomber_adv/bomber_adv.json": "hornet_count",
            "/pa/units/air/fabrication_aircraft/fabrication_aircraft.json": "fabrication_aircraft_count",
            "/pa/units/air/fabrication_aircraft_adv/fabrication_aircraft_adv.json": "advanced_fabrication_aircraft_count",
            "/pa/units/air/fighter/fighter.json": "hummingbird_count",
            "/pa/units/air/fighter_adv/fighter_adv.json": "phoenix_count",
            "/pa/units/air/gunship/gunship.json": "kestrel_count",
            "/pa/units/air/transport/transport.json": "pelican_count",
            "/pa/units/commanders/avatar/avatar.json": "avatar_count",
            "/pa/units/commanders/imperial_able/imperial_able.json": "able_count",
            "/pa/units/commanders/imperial_aceal/imperial_aceal.json": "aceal_count",
            "/pa/units/commanders/imperial_alpha/imperial_alpha.json": "alpha_count",
            "/pa/units/commanders/imperial_aryst0krat/imperial_aryst0krat.json": "aryst0krat_count",
            "/pa/units/commanders/imperial_base/imperial_base.json": "base_count",
            "/pa/units/commanders/imperial_chronoblip/imperial_chronoblip.json": "chronoblip_count",
            "/pa/units/commanders/imperial_delta/imperial_delta.json": "delta_count",
            "/pa/units/commanders/imperial_enzomatrix/imperial_enzomatrix.json": "enzomatrix_count",
            "/pa/units/commanders/imperial_fiveleafclover/imperial_fiveleafclover.json": "fiveleafclover_count",
            "/pa/units/commanders/imperial_fusion/imperial_fusion.json": "fusion_count",
            "/pa/units/commanders/imperial_gamma/imperial_gamma.json": "gamma_count",
            "/pa/units/commanders/imperial_gnugfur/imperial_gnugfur.json": "gnugfur_count",
            "/pa/units/commanders/imperial_invictus/imperial_invictus.json": "invictus_count",
            "/pa/units/commanders/imperial_jt100010117/imperial_jt100010117.json": "jt100010117_count",
            "/pa/units/commanders/imperial_kapowaz/imperial_kapowaz.json": "kapowaz_count",
            "/pa/units/commanders/imperial_kevin4001/imperial_kevin4001.json": "kevin4001_count",
            "/pa/units/commanders/imperial_mjon/imperial_mjon.json": "mjon_count",
            "/pa/units/commanders/imperial_mostlikely/imperial_mostlikely.json": "mostlikely_count",
            "/pa/units/commanders/imperial_nagasher/imperial_nagasher.json": "nagasher_count",
            "/pa/units/commanders/imperial_progenitor/imperial_progenitor.json": "progenitor_count",
            "/pa/units/commanders/imperial_sangudo/imperial_sangudo.json": "sangudo_count",
            "/pa/units/commanders/imperial_seniorhelix/imperial_seniorhelix.json": "seniorhelix_count",
            "/pa/units/commanders/imperial_stelarch/imperial_stelarch.json": "stelarch_count",
            "/pa/units/commanders/imperial_thechessknight/imperial_thechessknight.json": "thechessknight_count",
            "/pa/units/commanders/imperial_theta/imperial_theta.json": "theta_count",
            "/pa/units/commanders/imperial_toddfather/imperial_toddfather.json": "toddfather_count",
            "/pa/units/commanders/imperial_tykus24/imperial_tykus24.json": "tykus24_count",
            "/pa/units/commanders/imperial_vidicarus/imperial_vidicarus.json": "vidicarus_count",
            "/pa/units/commanders/imperial_visionik/imperial_visionik.json": "visionik_count",
            "/pa/units/commanders/quad_ajax/quad_ajax.json": "ajax_count",
            "/pa/units/commanders/quad_armalisk/quad_armalisk.json": "armalisk_count",
            "/pa/units/commanders/quad_base/quad_base.json": "base_count",
            "/pa/units/commanders/quad_calyx/quad_calyx.json": "calyx_count",
            "/pa/units/commanders/quad_commandonut/quad_commandonut.json": "commandonut_count",
            "/pa/units/commanders/quad_gambitdfa/quad_gambitdfa.json": "gambitdfa_count",
            "/pa/units/commanders/quad_locust/quad_locust.json": "quad_locust_count",
            "/pa/units/commanders/quad_mobiousblack/quad_mobiousblack.json": "mobiousblack_count",
            "/pa/units/commanders/quad_osiris/quad_osiris.json": "osiris_count",
            "/pa/units/commanders/quad_potbelly79/quad_potbelly79.json": "potbelly79_count",
            "/pa/units/commanders/quad_pumpkin/quad_pumpkin.json": "pumpkin_count",
            "/pa/units/commanders/quad_raventhornn/quad_raventhornn.json": "raventhornn_count",
            "/pa/units/commanders/quad_sacrificiallamb/quad_sacrificiallamb.json": "sacrificiallamb_count",
            "/pa/units/commanders/quad_shadowdaemon/quad_shadowdaemon.json": "shadowdaemon_count",
            "/pa/units/commanders/quad_spartandano/quad_spartandano.json": "spartandano_count",
            "/pa/units/commanders/quad_spiderofmean/quad_spiderofmean.json": "spiderofmean_count",
            "/pa/units/commanders/quad_theflax/quad_theflax.json": "theflax_count",
            "/pa/units/commanders/quad_tokamaktech/quad_tokamaktech.json": "tokamaktech_count",
            "/pa/units/commanders/quad_twoboots/quad_twoboots.json": "twoboots_count",
            "/pa/units/commanders/quad_xenosentryprime/quad_xenosentryprime.json": "xenosentryprime_count",
            "/pa/units/commanders/quad_xinthar/quad_xinthar.json": "xinthar_count",
            "/pa/units/commanders/quad_zancrowe/quad_zancrowe.json": "zancrowe_count",
            "/pa/units/commanders/raptor_base/raptor_base.json": "base_count",
            "/pa/units/commanders/raptor_beast/raptor_beast.json": "beast_count",
            "/pa/units/commanders/raptor_beast_king/raptor_beast_king.json": "beniesk_count",
            "/pa/units/commanders/raptor_beniesk/raptor_beniesk.json": "betadyne_count",
            "/pa/units/commanders/raptor_betadyne/raptor_betadyne.json": "centurion_count",
            "/pa/units/commanders/raptor_centurion/raptor_centurion.json": "damubbster_count",
            "/pa/units/commanders/raptor_damubbster/raptor_damubbster.json": "diremachine_count",
            "/pa/units/commanders/raptor_diremachine/raptor_diremachine.json": "enderstryke71_count",
            "/pa/units/commanders/raptor_enderstryke71/raptor_enderstryke71.json": "iwmiked_count",
            "/pa/units/commanders/raptor_iwmiked/raptor_iwmiked.json": "majuju_count",
            "/pa/units/commanders/raptor_majuju/raptor_majuju.json": "nefelpitou_count",
            "/pa/units/commanders/raptor_nefelpitou/raptor_nefelpitou.json": "nemicus_count",
            "/pa/units/commanders/raptor_nemicus/raptor_nemicus.json": "raizell_count",
            "/pa/units/commanders/raptor_raizell/raptor_raizell.json": "rallus_count",
            "/pa/units/commanders/raptor_rallus/raptor_rallus.json": "spz58624_count",
            "/pa/units/commanders/raptor_spz58624/raptor_spz58624.json": "stickman9000_count",
            "/pa/units/commanders/raptor_stickman9000/raptor_stickman9000.json": "unicorn_count",
            "/pa/units/commanders/raptor_unicorn/raptor_unicorn.json": "xov_count",
            "/pa/units/commanders/raptor_xov/raptor_xov.json": "zaazzaa_count",
            "/pa/units/commanders/raptor_zaazzaa/raptor_zaazzaa.json": "aeson_count",
            "/pa/units/commanders/tank_aeson/tank_aeson.json": "banditks_count",
            "/pa/units/commanders/tank_banditks/tank_banditks.json": "base_count",
            "/pa/units/commanders/tank_reaver/tank_reaver.json": "reaver_count",
            "/pa/units/commanders/tank_sadiga/tank_sadiga.json": "sadiga_count",
            "/pa/units/land/aa_missile_vehicle/aa_missile_vehicle.json": "spinner_count",
            "/pa/units/land/air_defense/air_defense.json": "galata_turret_count",
            "/pa/units/land/air_defense_adv/air_defense_adv.json": "flak_cannon_count",
            "/pa/units/land/anti_nuke_launcher/anti_nuke_launcher.json": "anti_nuke_launcher_count",
            "/pa/units/land/artillery_long/artillery_long.json": "holkins_count",
            "/pa/units/land/artillery_short/artillery_short.json": "pelter_count",
            "/pa/units/land/assault_bot/assault_bot.json": "dox_count",
            "/pa/units/land/assault_bot_adv/assault_bot_adv.json": "slammer_count",
            "/pa/units/land/bot_aa/bot_aa.json": "stinger_count",
            "/pa/units/land/bot_bomb/bot_bomb.json": "boom_count",
            "/pa/units/land/bot_factory/bot_factory.json": "bot_factory_count",
            "/pa/units/land/bot_factory_adv/bot_factory_adv.json": "advanced_bot_factory_count",
            "/pa/units/land/bot_grenadier/bot_grenadier.json": "grenadier_count",
            "/pa/units/land/bot_sniper/bot_sniper.json": "gil_e_count",
            "/pa/units/land/bot_tactical_missile/bot_tactical_missile.json": "bluehawk_count",
            "/pa/units/land/control_module/control_module.json": "catalyst_count",
            "/pa/units/land/energy_plant/energy_plant.json": "energy_plant_count",
            "/pa/units/land/energy_plant_adv/energy_plant_adv.json": "advanced_energy_plant_count",
            "/pa/units/land/energy_storage/energy_storage.json": "energy_storage_count",
            "/pa/units/land/fabrication_bot/fabrication_bot.json": "fabrication_bot_count",
            "/pa/units/land/fabrication_bot_adv/fabrication_bot_adv.json": "advanced_fabrication_bot_count",
            "/pa/units/land/fabrication_bot_combat/fabrication_bot_combat.json": "stitch_count",
            "/pa/units/land/fabrication_bot_combat_adv/fabrication_bot_combat_adv.json": "mend_count",
            "/pa/units/land/fabrication_vehicle/fabrication_vehicle.json": "fabrication_vehicle_count",
            "/pa/units/land/fabrication_vehicle_adv/fabrication_vehicle_adv.json": "advanced_fabrication_vehicle_count",
            "/pa/units/land/land_barrier/land_barrier.json": "wall_count",
            "/pa/units/land/land_mine/land_mine.json": "mine_count",
            "/pa/units/land/land_scout/land_scout.json": "skitter_count",
            "/pa/units/land/laser_defense/laser_defense.json": "laser_defense_tower_count",
            "/pa/units/land/laser_defense_adv/laser_defense_adv.json": "advanced_laser_defense_tower_count",
            "/pa/units/land/laser_defense_single/laser_defense_single.json": "single_laser_defense_tower_count",
            "/pa/units/land/metal_extractor/metal_extractor.json": "metal_extractor_count",
            "/pa/units/land/metal_extractor_adv/metal_extractor_adv.json": "advanced_metal_extractor_count",
            "/pa/units/land/metal_storage/metal_storage.json": "metal_storage_count",
            "/pa/units/land/nuke_launcher/nuke_launcher.json": "nuclear_missile_launcher_count",
            "/pa/units/land/radar/radar.json": "radar_count",
            "/pa/units/land/radar_adv/radar_adv.json": "advanced_radar_count",
            "/pa/units/land/tactical_missile_launcher/tactical_missile_launcher.json": "catapult_count",
            "/pa/units/land/tank_armor/tank_armor.json": "inferno_count",
            "/pa/units/land/tank_heavy_armor/tank_heavy_armor.json": "vanguard_count",
            "/pa/units/land/tank_heavy_mortar/tank_heavy_mortar.json": "sheller_count",
            "/pa/units/land/tank_laser_adv/tank_laser_adv.json": "leveler_count",
            "/pa/units/land/tank_light_laser/tank_light_laser.json": "ant_count",
            "/pa/units/land/teleporter/teleporter.json": "teleporter_count",
            "/pa/units/land/unit_cannon/unit_cannon.json": "unit_cannon_count",
            "/pa/units/land/vehicle_factory/vehicle_factory.json": "vehicle_factory_count",
            "/pa/units/land/vehicle_factory_adv/vehicle_factory_adv.json": "advanced_vehicle_factory_count",
            "/pa/units/orbital/deep_space_radar/deep_space_radar.json": "orbital_and_deepspace_radar_count",
            "/pa/units/orbital/defense_satellite/defense_satellite.json": "anchor_count",
            "/pa/units/orbital/delta_v_engine/delta_v_engine.json": "halley_count",
            "/pa/units/orbital/ion_defense/ion_defense.json": "umbrella_count",
            "/pa/units/orbital/mining_platform/mining_platform.json": "jig_count",
            "/pa/units/orbital/orbital_fabrication_bot/orbital_fabrication_bot.json": "orbital_fabrication_bot_count",
            "/pa/units/orbital/orbital_factory/orbital_factory.json": "orbital_factory_count",
            "/pa/units/orbital/orbital_fighter/orbital_fighter.json": "avenger_count",
            "/pa/units/orbital/orbital_lander/orbital_lander.json": "astraeus_count",
            "/pa/units/orbital/orbital_laser/orbital_laser.json": "sxx_1304_laser_platform_count",
            "/pa/units/orbital/orbital_launcher/orbital_launcher.json": "orbital_launcher_count",
            "/pa/units/orbital/radar_satellite/radar_satellite.json": "advanced_radar_satellite_count",
            "/pa/units/orbital/radar_satellite_adv/radar_satellite_adv.json": "arkyd_count",
            "/pa/units/orbital/solar_array/solar_array.json": "solar_array_count",
            "/pa/units/sea/attack_sub/attack_sub.json": "barracuda_count",
            "/pa/units/sea/battleship/battleship.json": "leviathan_count",
            "/pa/units/sea/destroyer/destroyer.json": "orca_count",
            "/pa/units/sea/fabrication_ship/fabrication_ship.json": "fabrication_ship_count",
            "/pa/units/sea/fabrication_ship_adv/fabrication_ship_adv.json": "advanced_fabrication_ship_count",
            "/pa/units/sea/frigate/frigate.json": "narwhal_count",
            "/pa/units/sea/missile_ship/missile_ship.json": "stingray_count",
            "/pa/units/sea/naval_factory/naval_factory.json": "naval_factory_count",
            "/pa/units/sea/naval_factory_adv/naval_factory_adv.json": "advanced_naval_factory_count",
            "/pa/units/sea/nuclear_sub/nuclear_sub.json": "kraken_count",
            "/pa/units/sea/sea_scout/sea_scout.json": "piranha_count",
            "/pa/units/sea/torpedo_launcher/torpedo_launcher.json": "torpedo_launcher_count",
            "/pa/units/sea/torpedo_launcher_adv/torpedo_launcher_adv.json": "advanced_torpedo_launcher_count",
            "/pa/units/air/bomber_heavy/bomber_heavy.json": "wyrm_count",
            "/pa/units/air/solar_drone/solar_drone.json": "icarus_count",
            "/pa/units/air/strafer/strafer.json": "horsefly_count",
            "/pa/units/air/support_platform/support_platform.json": "angel_count",
            "/pa/units/air/titan_air/titan_air.json": "zeus_count",
            "/pa/units/land/artillery_unit_launcher/artillery_unit_launcher.json": "lob_count",
            "/pa/units/land/attack_vehicle/attack_vehicle.json": "stryker_count",
            "/pa/units/land/bot_nanoswarm/bot_nanoswarm.json": "locust_count",
            "/pa/units/land/bot_support_commander/bot_support_commander.json": "colonel_count",
            "/pa/units/land/bot_tesla/bot_tesla.json": "spark_count",
            "/pa/units/land/tank_flak/tank_flak.json": "storm_count",
            "/pa/units/land/tank_hover/tank_hover.json": "drifter_count",
            "/pa/units/land/tank_nuke/tank_nuke.json": "manhattan_count",
            "/pa/units/land/titan_bot/titan_bot.json": "atlas_count",
            "/pa/units/land/titan_structure/titan_structure.json": "ragnarok_count",
            "/pa/units/land/titan_vehicle/titan_vehicle.json": "ares_count",
            "/pa/units/orbital/orbital_battleship/orbital_battleship.json": "omega_count",
            "/pa/units/orbital/orbital_probe/orbital_probe.json": "hermes_count",
            "/pa/units/orbital/orbital_railgun/orbital_railgun.json": "artemis_count",
            "/pa/units/orbital/titan_orbital/titan_orbital.json": "helios_count",
            "/pa/units/sea/drone_carrier/carrier/carrier.json": "typhoon_count",
            "/pa/units/sea/drone_carrier/drone/drone.json": "squall_count",
            "/pa/units/sea/fabrication_barge/fabrication_barge.json": "barnacle_count",
            "/pa/units/sea/hover_ship/hover_ship.json": "kaiju_count",
            "/pa/units/land/radar_jammer/radar_jammer.json": "radar_jamming_station_count"}

        list_units_buildings_data = unb_data

        for i in range(len(list_units_buildings_data)):
            if len(list_units_buildings_data[i]) > 2:
                json_list_unb = json.loads(list_units_buildings_data[i])
                for path_unb in json_list_unb.keys():
                    if path_unb in full_list_unb:
                        setattr(
                            self,
                            full_list_unb[path_unb],
                            int(getattr(self, full_list_unb[path_unb])) + len(json_list_unb[path_unb]))
                    else:
                        print(f"Key {path_unb} not found in full_list_unb.")
                print("ok")
                self.save()

# class UnitsBuildingsCountLegion(models.Model):
# class UnitsBuildingsCountSecondWave(models.Model):
# class UnitsBuildingsCountThorosmen(models.Model):
# class UnitsBuildingsCountS17(models.Model):
# class UnitsBuildingsBugs(models.Model):
# class UnitsBuildingsCountOthersMods(models.Model):


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

    def check_n_save(self, eco_data, current_apm, lobby_id, uber_id, time_data):
        # EnergyGain, EnergyLoss, EnergyNet, EnergyEfficiencyPerc, EnergyCurrentEnergy, EnergyMaxEnergy, MetalGain,
        # MetalLoss, MetalNet, MetalEfficiencyPerc, MetalCurrentMetal, MetalMaxMetal
        self.apm_data = current_apm
        self.lobby_id = lobby_id
        self.uber_id = uber_id
        self.current_time = int(time_data)

        if len(eco_data) >= 12:
            self.energy_gain = eco_data[0]
            self.energy_loss = eco_data[1]
            self.energy_net = eco_data[2]
            if round(eco_data[3], 2) > 1:
                self.energy_efficiency_perc = 100
            else:
                self.energy_efficiency_perc = round(eco_data[3], 2)*100
            self.energy_current_energy = eco_data[4]
            self.energy_max_energy = eco_data[5]
            self.metal_gain = eco_data[6]
            self.metal_loss = eco_data[7]
            self.metal_net = eco_data[8]
            if round(eco_data[9], 2) > 1:
                self.metal_efficiency_perc = 100
            else:
                self.metal_efficiency_perc = round(eco_data[9], 2)*100

            self.metal_current_metal = eco_data[10]
            self.metal_max_metal = eco_data[11]

            self.metal_win_rate = eco_data[12]
            self.metal_loss_rate = eco_data[13]

            if self.metal_current_metal == self.metal_max_metal:
                self.metal_wasted = self.metal_gain
            else:
                self.metal_wasted = 0

            if self.energy_current_energy == self.energy_max_energy:
                self.energy_wasted = self.energy_gain
            else:
                self.energy_wasted = 0

            previous_metal_produced = GamesEconomyApm.objects.filter(lobby_id=self.lobby_id).aggregate(Sum('metal_gain'))[
                                          'metal_gain__sum'] or 0
            self.metal_produced = previous_metal_produced + self.metal_gain

            # Calculate energy_produced
            previous_energy_produced = GamesEconomyApm.objects.filter(lobby_id=self.lobby_id).aggregate(Sum('energy_gain'))[
                                           'energy_gain__sum'] or 0
            self.energy_produced = previous_energy_produced + self.energy_gain

            if round(self.energy_efficiency_perc, 2) > 100:
                eef = 100
            elif round(self.energy_efficiency_perc, 2) == 10:
                eef = 100
            elif round(self.energy_efficiency_perc, 2) > 1:
                eef = 100
            else:
                eef = round(self.energy_efficiency_perc, 2)*100

            if round(self.metal_efficiency_perc, 2) > 100:
                mef = 100
            elif round(self.metal_efficiency_perc, 2) == 10:
                mef = 100
            elif round(self.metal_efficiency_perc, 2) > 1 :
                mef = 100
            else:
                mef = round(self.metal_efficiency_perc, 2)*100

            self.efficiency = round((eef * mef)/100, 2)

        self.save()
