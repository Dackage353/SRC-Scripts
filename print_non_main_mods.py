from common import fetch_handler, file_helper, reference, src_helper, tool, constants
import time


script_start = time.perf_counter()

FORCE_FETCH = False

MAIN_MODS = {
     'zxzlkr08', #AndrewSM64
     '68wzrnv8', #aussieadam
     'qxkrpqm8', #Dackage
     'kj957778', #DJ_Tala
     'pj0n70m8', #FrostyZako
     'v8lyv4jm', #MarvJungs
     'v8lk144x', #Phanton
     'qjopronx' #Tomatobird8
}


if __name__ == '__main__':
    data = fetch_handler.get_series_info(constants.MAIN_SERIES, FORCE_FETCH)
    data.extend(fetch_handler.get_series_info(constants.SECONDARY_SERIES, FORCE_FETCH))

    for game_data in data:
        potential_incorrect_mods = []

        for mod in game_data['moderators']:
            if mod not in MAIN_MODS:
                name = fetch_handler.get_user_name(mod)
                potential_incorrect_mods.append(name)

        if potential_incorrect_mods:
                print(f"{game_data['abbreviation']} has non-main mods of {potential_incorrect_mods}")

    script_end = time.perf_counter()
    print(f"\nElapsed time: {script_end - script_start:.2f} seconds")
    