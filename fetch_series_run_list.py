from common import fetch_handler, file_helper, reference, src_helper, tool, constants

FORCE_FETCH = False

if __name__ == '__main__':
    series_run_list = fetch_handler.get_series_run_list(constants.SECONDARY_SERIES, FORCE_FETCH)
    print(f'series run list is size {len(series_run_list)}')
