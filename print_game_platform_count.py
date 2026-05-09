from common import fetch_handler, file_helper, reference, src_helper, tool, constants
import time


script_start = time.perf_counter()

FORCE_FETCH = False


if __name__ == '__main__':
    data = fetch_handler.get_series_info(constants.MAIN_SERIES, FORCE_FETCH)
    data.extend(fetch_handler.get_series_info(constants.SECONDARY_SERIES, FORCE_FETCH))

    games_with_1 = []
    games_with_2 = []
    games_with_3 = []
    other_games = []

    for game_data in data:
        platforms = game_data.get('platforms')

        name = game_data.get('names', {}).get('international')
        if len(platforms) == 1:
            games_with_1.append(name)
        elif len(platforms) == 2:
            games_with_2.append(name)
        elif len(platforms) == 3:
            games_with_3.append(name)

    print('games with 1 platform\n-----')
    print('\n'.join(games_with_1))

    print('\ngames with 2 platforms\n-----')
    print('\n'.join(games_with_2))

    print('\ngames with 3 platforms\n-----')
    print('\n'.join(games_with_3))

    #print('\games without 1-3 platforms\n-----')
    #print('\n'.join(other_games))

    print(f'\n{len(games_with_1)} have 1 platform')
    print(f'{len(games_with_2)} have 2 platforms')
    print(f'{len(games_with_3)} have 3 platforms')
    #print(f'{len(other_games)} without 1-3 platforms')

    script_end = time.perf_counter()
    print(f"\nElapsed time: {script_end - script_start:.2f} seconds")
    