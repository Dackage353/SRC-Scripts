import common.data_classes as data_classes
import common.file_handler as file_handler

main_mods = {
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
    games = file_handler.fetch_rom_hack_info_list()

    for game in games:
        potential_incorrect_mods = []

        for mod in game['moderators']:
            if mod not in main_mods:
                name = file_handler.fetch_user_name(mod)
                potential_incorrect_mods.append(name)

        if potential_incorrect_mods:
                print(f"{game['abbreviation']} has non-main mods of {potential_incorrect_mods}")

                
