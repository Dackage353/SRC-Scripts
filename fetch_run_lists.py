from common import fetch_handler, file_helper, reference, src_helper, tool, constants
import time


script_start = time.perf_counter()

FORCE_FETCH = False


if __name__ == '__main__':
    main_series_run_list = fetch_handler.get_series_run_list(constants.MAIN_SERIES, FORCE_FETCH)
    secondary_series_run_list = fetch_handler.get_series_run_list(constants.SECONDARY_SERIES, FORCE_FETCH)
    
    print(f'main series run list is size {len(main_series_run_list)}')    
    print(f'secondary series run list is size {len(secondary_series_run_list)}')
    
    script_end = time.perf_counter()
    print(f"\nElapsed time: {script_end - script_start:.2f} seconds")
