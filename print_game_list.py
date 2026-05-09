from common import fetch_handler, file_helper, reference, src_helper, tool, constants
import time


script_start = time.perf_counter()

FORCE_FETCH = False


if __name__ == '__main__':
    hack_names = fetch_handler.get_series_game_names(constants.MAIN_SERIES, FORCE_FETCH)
    hack_names.extend(fetch_handler.get_series_game_names(constants.SECONDARY_SERIES, FORCE_FETCH))
    hack_names.sort()

    print('\n'.join(hack_names))
    
    script_end = time.perf_counter()
    print(f"\nElapsed time: {script_end - script_start:.2f} seconds")
