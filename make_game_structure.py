from common import fetch_handler, file_helper, reference, src_helper, tool, constants



FORCE_FETCH = False

if __name__ == '__main__':
    game_data = fetch_handler.fetch_series_info(FORCE_FETCH, constants.MAIN_SERIES)
    game_data.extend(fetch_handler.fetch_series_info(FORCE_FETCH, constants.SECONDARY_SERIES))

    print(len(game_data))