from common import fetch_handler, file_helper, reference, src_helper, tool, constants


FORCE_FETCH = False


if __name__ == '__main__':
    hack_names = fetch_handler.get_series_game_names(constants.MAIN_SERIES, FORCE_FETCH)
    hack_names.extend(fetch_handler.get_series_game_names(constants.SECONDARY_SERIES, FORCE_FETCH))
    hack_names.sort()

    print('\n'.join(hack_names))
