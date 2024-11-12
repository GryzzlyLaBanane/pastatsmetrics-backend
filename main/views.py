from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from .models import (LobbyData, UnitsBuildingsCountMLA, GamesEconomyApm, KillsData, PlayersGamesHistory,
                     PlayerNameListData)
from .forms import SearchForm
from django.db.models import Q
import ast
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

def pastats(request):
    return render(request, "main/research.html")


@csrf_exempt
def lobbydata_receiver(request):
    if request.method == 'POST':
        raw_lobby_data = request.body.decode("utf-8")
        lobby_data = json.loads(raw_lobby_data)
        new_lobby_to_save = LobbyData()
        new_lobby_to_save.check_n_save(lobby_data)
    return JsonResponse({'message': 'Data received'}, status=200)


@csrf_exempt
def gamedata_receiver(request):
    if request.method == 'POST':
        raw_game_data = request.body.decode("utf-8")
        all_data = json.loads(raw_game_data)

        lobby_id = all_data.get("lobby_id")
        uber_id = all_data.get("uber_id")
        if not lobby_id:
            return JsonResponse({'error': 'lobby_id is required'}, status=400)
        lobby_instance, created = LobbyData.objects.get_or_create(lobby_id=lobby_id)
        lobby_instance.update_lobby_data(all_data)

        uber_id = all_data.get("uber_id")
        time_data = all_data.get("time_in_seconds")
        unb_data = all_data.get("unb_data")
        units_buildings = UnitsBuildingsCountMLA()
        units_buildings.check_n_save(lobby_id, uber_id, time_data, unb_data)

        eco_of_the_game = GamesEconomyApm()
        eco_of_the_game.check_n_save(all_data.get("eco_data"),
                                     all_data.get("current_apm"),
                                     lobby_id,
                                     uber_id,
                                     time_data)

        kill_data = all_data.get("kill_data")
        kill_data_to_save = KillsData()
        kill_data_to_save.check_n_save(kill_data, lobby_id, time_data)

        game_hist = PlayersGamesHistory()
        game_hist.check_n_save(lobby_id, uber_id, all_data.get("player_name"))

        name_hist = PlayerNameListData()
        name_hist.check_n_save(uber_id, all_data.get("player_name"), all_data.get("the_date"))

        # print(raw_game_data)
    return JsonResponse({'message': 'Data received'}, status=200)

def search_players(request):
    query = request.GET.get('query', '')
    fields = request.GET.get('fields', '').split(',')
    if query and fields:
        q_objects = Q()
        if 'lobby_id' in fields:
            q_objects |= Q(lobby_id__icontains=query)
        if 'uber_id' in fields:
            q_objects |= Q(uber_id__icontains=query)
        if 'player_name' in fields:
            q_objects |= Q(player_name__icontains=query)
        if 'player_list' in fields:
            q_objects |= Q(player_list__icontains=query)
        if 'user_name' in fields:
            q_objects |= Q(user_name__icontains=query)
        if 'system_name' in fields:
            q_objects |= Q(system_name__icontains=query)
        print("turbo teuuuuuuub ----------------------------------------------", fields)
        matching_entries = LobbyData.objects.filter(q_objects)

        # Feature pour plus tard, en gros si on chercher un nom, on obtiens que les game avec ce nom mais pas tt les
        # du player, donc faut à partir du nom trouver le uber ID puis matcher tt ses games, si le
        # gars change de nom à chaque game ben pour l'isntant que voit que 1 game par 1 game
        # if 'player_list' in fields:
        #     for entry in matching_entries:
        #         try:
        #             player_list_data = json.loads(entry.player_list)
        #             for player_name, player_data in player_list_data.items():
        #                 if query in player_name or query in player_data:
        #                     uber_ids.add(entry.uber_id)
        #         except json.JSONDecodeError:
        #             continue

        results = []
        for entry in matching_entries:
            winners_list = ast.literal_eval(entry.winners)
            winners_str = ""
            if winners_list :
                for i in range(len(winners_list)):
                    if i == len(winners_list)-1:
                        winners_str += winners_list[i]
                    else:
                        winners_str += winners_list[i] + ", "
            else :
                winners_str = "No Known Winners"
            results.append({
                'lobby_id': entry.lobby_id,
                'uber_id': entry.uber_id,
                'player_name': entry.player_name,
                'user_name': entry.user_name,
                'system_name': entry.system_name,
                'player_list': entry.player_list,
                'date_game_start': entry.date_game_start,
                'date_game_last': entry.date_game_last,
                'game_mode': entry.game_mode,
                'player_count': entry.player_count,
                'winners': winners_str
            })

        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)


def charts(request, lobby_id):
    lobby_data = lobby_id #get_object_or_404(LobbyData, lobby_id=lobby_id)
    return render(request, 'main/charts.html',
                  {'lobby_data': lobby_data})


def get_charts(request):
    unit_types = {
        "air_factory_count": ["building", "factory"],
        "advanced_air_factory_count": ["building", "factory"],
        "firefly_count": ["air"],
        "bumblebee_count": ["air"],
        "hornet_count": ["air"],
        "fabrication_aircraft_count": ["fabber"],
        "advanced_fabrication_aircraft_count": ["fabber"],
        "hummingbird_count": ["air"],
        "phoenix_count": ["air"],
        "kestrel_count": ["air"],
        "pelican_count": ["air"],
        "able_count": ["commander"],
        "aceal_count": ["commander"],
        "alpha_count": ["commander"],
        "aryst0krat_count": ["commander"],
        "chronoblip_count": ["commander"],
        "delta_count": ["commander"],
        "enzomatrix_count": ["commander"],
        "fiveleafclover_count": ["commander"],
        "fusion_count": ["commander"],
        "gamma_count": ["commander"],
        "gnugfur_count": ["commander"],
        "invictus_count": ["commander"],
        "jt100010117_count": ["commander"],
        "kapowaz_count": ["commander"],
        "kevin4001_count": ["commander"],
        "mjon_count": ["commander"],
        "mostlikely_count": ["commander"],
        "nagasher_count": ["commander"],
        "progenitor_count": ["commander"],
        "sangudo_count": ["commander"],
        "seniorhelix_count": ["commander"],
        "stelarch_count": ["commander"],
        "thechessknight_count": ["commander"],
        "theta_count": ["commander"],
        "toddfather_count": ["commander"],
        "tykus24_count": ["commander"],
        "vidicarus_count": ["commander"],
        "visionik_count": ["commander"],
        "ajax_count": ["commander"],
        "armalisk_count": ["commander"],
        "base_count": ["commander"],
        "calyx_count": ["commander"],
        "commandonut_count": ["commander"],
        "gambitdfa_count": ["commander"],
        "quad_locust_count": ["commander"],
        "mobiousblack_count": ["commander"],
        "osiris_count": ["commander"],
        "potbelly79_count": ["commander"],
        "pumpkin_count": ["commander"],
        "raventhornn_count": ["commander"],
        "sacrificiallamb_count": ["commander"],
        "shadowdaemon_count": ["commander"],
        "spartandano_count": ["commander"],
        "spiderofmean_count": ["commander"],
        "theflax_count": ["commander"],
        "tokamaktech_count": ["commander"],
        "twoboots_count": ["commander"],
        "xenosentryprime_count": ["commander"],
        "xinthar_count": ["commander"],
        "zancrowe_count": ["commander"],
        "beast_count": ["commander"],
        "beniesk_count": ["commander"],
        "betadyne_count": ["commander"],
        "centurion_count": ["commander"],
        "damubbster_count": ["commander"],
        "diremachine_count": ["commander"],
        "enderstryke71_count": ["commander"],
        "iwmiked_count": ["commander"],
        "majuju_count": ["commander"],
        "nefelpitou_count": ["commander"],
        "nemicus_count": ["commander"],
        "raizell_count": ["commander"],
        "rallus_count": ["commander"],
        "spz58624_count": ["commander"],
        "stickman9000_count": ["commander"],
        "unicorn_count": ["commander"],
        "xov_count": ["commander"],
        "zaazzaa_count": ["commander"],
        "aeson_count": ["commander"],
        "banditks_count": ["commander"],
        "reaver_count": ["commander"],
        "sadiga_count": ["commander"],
        "spinner_count": ["tank", "land"],
        "galata_turret_count": ["building"],
        "flak_cannon_count": ["building"],
        "anti_nuke_launcher_count": ["building"],
        "holkins_count": ["building"],
        "pelter_count": ["building"],
        "dox_count": ["bot", "land"],
        "slammer_count": ["bot", "land"],
        "stinger_count": ["bot", "land"],
        "boom_count": ["bot", "land"],
        "bot_factory_count": ["building", "factory"],
        "advanced_bot_factory_count": ["building", "factory"],
        "grenadier_count": ["bot", "land"],
        "gil_e_count": ["bot", "land"],
        "bluehawk_count": ["bot", "land"],
        "catalyst_count": ["building"],
        "energy_plant_count": ["building"],
        "advanced_energy_plant_count": ["building"],
        "energy_storage_count": ["building"],
        "fabrication_bot_count": ["fabber"],
        "advanced_fabrication_bot_count": ["fabber"],
        "stitch_count": ["bot", "land"],
        "mend_count": ["bot", "land"],
        "fabrication_vehicle_count": ["fabber"],
        "advanced_fabrication_vehicle_count": ["fabber"],
        "wall_count": ["building"],
        "mine_count": ["building"],
        "skitter_count": ["tank", "land"],
        "laser_defense_tower_count": ["building"],
        "advanced_laser_defense_tower_count": ["building"],
        "single_laser_defense_tower_count": ["building"],
        "metal_extractor_count": ["building"],
        "advanced_metal_extractor_count": ["building"],
        "metal_storage_count": ["building"],
        "nuclear_missile_launcher_count": ["building"],
        "radar_count": ["building"],
        "advanced_radar_count": ["building"],
        "catapult_count": ["building"],
        "inferno_count": ["tank", "land"],
        "vanguard_count": ["tank", "land"],
        "sheller_count": ["tank", "land"],
        "leveler_count": ["tank", "land"],
        "ant_count": ["tank", "land"],
        "teleporter_count": ["building"],
        "unit_cannon_count": ["building"],
        "vehicle_factory_count": ["building", "factory"],
        "advanced_vehicle_factory_count": ["building", "factory"],
        "orbital_and_deepspace_radar_count": ["building"],
        "anchor_count": ["building"],
        "halley_count": ["building"],
        "umbrella_count": ["building"],
        "jig_count": ["building"],
        "orbital_fabrication_bot_count": ["fabber"],
        "orbital_factory_count": ["building", "factory"],
        "avenger_count": ["orbital"],
        "astraeus_count": ["orbital"],
        "sxx_1304_laser_platform_count": ["orbital"],
        "orbital_launcher_count": ["building", "factory"],
        "advanced_radar_satellite_count": ["orbital"],
        "arkyd_count": ["orbital"],
        "solar_array_count": ["orbital"],
        "barracuda_count": ["naval"],
        "leviathan_count": ["naval"],
        "orca_count": ["naval"],
        "fabrication_ship_count": ["fabber"],
        "advanced_fabrication_ship_count": ["fabber"],
        "narwhal_count": ["naval"],
        "stingray_count": ["naval"],
        "naval_factory_count": ["building", "factory"],
        "advanced_naval_factory_count": ["building", "factory"],
        "kraken_count": ["naval"],
        "piranha_count": ["naval"],
        "torpedo_launcher_count": ["building"],
        "advanced_torpedo_launcher_count": ["building"],
        "wyrm_count": ["air"],
        "icarus_count": ["air"],
        "horsefly_count": ["air"],
        "angel_count": ["air"],
        "zeus_count": ["air"],
        "lob_count": ["building"],
        "stryker_count": ["tank", "land"],
        "locust_count": ["bot", "land"],
        "colonel_count": ["bot", "land", "fabber"],
        "spark_count": ["bot", "land"],
        "storm_count": ["tank", "land"],
        "drifter_count": ["tank", "land"],
        "manhattan_count": ["tank", "land"],
        "atlas_count": ["bot", "land"],
        "ragnarok_count": ["building"],
        "ares_count": ["tank", "land"],
        "omega_count": ["orbital"],
        "hermes_count": ["orbital"],
        "artemis_count": ["orbital"],
        "helios_count": ["orbital"],
        "typhoon_count": ["naval"],
        "squall_count": ["air"],
        "barnacle_count": ["naval"],
        "kaiju_count": ["naval"],
        "avatar_count": ["special"],
        "radar_jamming_station_count": ["building"]}
    clicked_buttons = request.GET.getlist('buttons')[0].split(",")
    lobby_id = request.GET.get('lobby_id')
    if not lobby_id:
        return JsonResponse({'error': 'Lobby ID is required'}, status=400)
    data = {'current_time': []}
    field_mapping = {
        'generalEfficiency': 'efficiency',
        'metalEfficiency': 'metal_efficiency_perc',
        'energyEfficiency': 'energy_efficiency_perc',
        'metalIncome': 'metal_gain',
        'metalUsage': 'metal_loss',
        'metalNet': 'metal_net',
        'metalStorage': 'metal_max_metal',
        'metalStored': 'metal_current_metal',
        'metalWinRate': 'metal_win_rate',
        'metalLossRate': 'metal_loss_rate',
        'metalWasted': 'metal_wasted',
        'metalProduced': 'metal_produced',
        'energyIncome': 'energy_gain',
        'energyUsage': 'energy_loss',
        'energyNet': 'energy_net',
        'energyStorage': 'energy_max_energy',
        'energyStored': 'energy_current_energy',
        'energyWasted': 'energy_wasted',
        'energyProduced': 'energy_produced',
        'totalBuildings': 'total_buildings',
        'totalFactory': 'total_factory',
        'totalFabbers': 'total_fabbers',
        'totalLand': 'total_land',
        'totalTank': 'total_tank',
        'totalBot': 'total_bot',
        'totalAir': 'total_air',
        'totalOrbital': 'total_orbital',
        'totalNaval': 'total_naval',
        'apmData': 'apm_data'
    }
    try:
        game_data = GamesEconomyApm.objects.filter(lobby_id=lobby_id).order_by('current_time', 'uber_id')
        data['current_time'] = list(sorted(set(game_data.values_list('current_time', flat=True))))

        lobby_data = get_object_or_404(LobbyData, lobby_id=lobby_id)
        player_list = json.loads(lobby_data.player_list)

        # fix du player history et player list pour avoir le player list avecd les bon UBERID et pas juste les vieux nom dégueux
        # il faudrait update la player_list de lobby data quand c'est une game local
        game_hist_data = PlayersGamesHistory.objects.filter(lobby_id=lobby_id)
        list_uber_id = []
        for player in player_list:
            for player_hist in game_hist_data:
                if player_hist.player_name == player:
                    player_list[player][0] = player_hist.uber_id
                    list_uber_id.append(player_hist.uber_id)

        for button in clicked_buttons:
            field_name = field_mapping.get(button)
            if field_name and button.startswith(('general', 'metal', 'energy', 'apm')):
                data[button] = {}
                players_data = game_data.values_list('uber_id', field_name)
                for uber_id, value in players_data:
                    if uber_id not in data[button]:
                        data[button][uber_id] = []
                    data[button][uber_id].append(value)



        unit_field_names = [field.name for field in UnitsBuildingsCountMLA._meta.fields if
                            field.name.endswith('_count')]

        # Define a mapping of buttons to their corresponding tags
        button_tag_mapping = {
            "totalBot": ["bot"],
            "totalTank": ["tank"],
            "totalAir": ["air"],
            "totalNaval": ["naval"],
            "totalOrbital": ["orbital"],
            "totalFabbers": ["fabber"],
            "totalFactory": ["factory"],
            "totalBuildings": ["building"],
            "totalLand": ["bot", "tank"],  # Sum of both bot and tank
            "totalUnits": ["air", "naval", "orbital", "bot", "tank"]  # Sum of all unit types
        }

        for button in clicked_buttons:
            if button in button_tag_mapping:
                data[button] = {}
                # Get the specific tags for the current button
                tags = button_tag_mapping.get(button, [])
                # Filter unit field names based on the tags for this button
                button_field_names = [name for name in unit_field_names if
                                      any(tag in unit_types.get(name, []) for tag in tags)]
                for iuber_id in list_uber_id:
                    data[button][iuber_id] = []
                    # Only calculate totals if there are relevant field names for this button
                    if button_field_names:
                        total_values = []
                        # Retrieve data for all relevant current_time values in one query
                        unit_data = UnitsBuildingsCountMLA.objects.filter(
                            lobby_id=lobby_id,
                            uber_id=iuber_id,
                            current_time__in=data['current_time']
                        ).order_by('current_time').values_list('current_time', *button_field_names)
                        # Convert to a dictionary for quick lookups by current_time
                        unit_data_dict = {item[0]: item[1:] for item in unit_data}
                        # Process each current_time, calculating sums based on the button's fields if data is available
                        for cut in data['current_time']:
                            if cut in unit_data_dict:
                                # Sum values for the button's relevant fields in this current_time entry
                                value_sum = sum(unit_data_dict[cut])
                                total_values.append(value_sum)
                            elif len(total_values) >= 1:
                                # Append the last value sum if no data found for the current_time
                                total_values.append(total_values[-1])
                        # Assign the calculated total_values list to the data structure
                        data[button][iuber_id] = total_values
                    else:
                        # If no relevant fields are found, assign an empty list
                        data[button][iuber_id] = []

        # Add player colors
        data['player_colors'] = {}
        for player_name, (uid, color) in player_list.items():
            data['player_colors'][uid] = color
        # Handle killsData
        if 'killsData' in clicked_buttons:
            kills_data = KillsData.objects.filter(lobby_id=lobby_id).order_by('time_kill')
            data['killsData'] = list(kills_data.values('time_kill', 'killer_name', 'defeated_name'))

    except GamesEconomyApm.DoesNotExist:
        return JsonResponse({'error': 'No data found for the given Lobby ID'}, status=404)
    except UnitsBuildingsCountMLA.DoesNotExist:
        return JsonResponse({'error': 'No data found for the given Lobby ID'}, status=404)
    return JsonResponse(data, safe=False)