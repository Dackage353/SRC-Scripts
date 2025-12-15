import common.file_handler as file_handler
import common.data_classes as data_classes

if __name__ == '__main__':
    data = file_handler.fetch_rom_hack_info_list()

    hacks = []

    for hack in data:
        hacks.append(data_classes.Game.create_from_json(hack))

    print(hacks)
