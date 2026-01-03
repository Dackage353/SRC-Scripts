from common import fetch_handler, file_helper, reference, src_helper, tool


FORCE_FETCH = False


if __name__ == '__main__':
    hack_names = fetch_handler.fetch_all_series_game_names(FORCE_FETCH)
    print('\n'.join(hack_names))
