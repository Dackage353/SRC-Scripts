from common import data_handler, fetch_handler, file_helper, reference


FORCE_FETCH = False

GAME_IDS = [
    'j1np0w6p'
]


if __name__ == '__main__':
    data = fetch_handler.fetch_game_info(GAME_IDS, FORCE_FETCH)
    #data = fetch_handler.fetch_all_hack_info(FORCE_FETCH)

    hacks = data_handler.create_game_info_from_data(data)

    for hack in hacks:
        print(hack.get_simple_text())
        print('\n\n')
