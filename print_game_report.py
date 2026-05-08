from common import fetch_handler, file_helper, reference, src_helper, tool, constants
from classes import Game


FORCE_FETCH = False


if __name__ == '__main__':
    game_data = fetch_handler.get_series_info(constants.MAIN_SERIES, FORCE_FETCH)
    game_data.extend(fetch_handler.get_series_info(constants.SECONDARY_SERIES, FORCE_FETCH))

    games = []

    for data in game_data:
        games.append(Game(data))

    for game in games:
        print(game.name)
        print('-----')

        for fullgame_category in game.fullgame_categories:
            print(fullgame_category.name)

        print()



