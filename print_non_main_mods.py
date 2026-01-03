from common import fetch_handler, file_helper, reference, src_helper, tool


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
    games = fetch_handler.fetch_all_hack_info(FORCE_FETCH)

    for game in games:
        potential_incorrect_mods = []

        for mod in game['moderators']:
            if mod not in MAIN_MODS:
                name = fetch_handler.fetch_user_name(mod)
                potential_incorrect_mods.append(name)

        if potential_incorrect_mods:
                print(f"{game['abbreviation']} has non-main mods of {potential_incorrect_mods}")
