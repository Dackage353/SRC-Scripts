from common import fetch_handler, file_helper, reference, src_helper, tool, constants


FORCE_FETCH = False


if __name__ == '__main__':
    main_series_run_list = fetch_handler.get_series_run_list(constants.MAIN_SERIES, FORCE_FETCH)
    secondary_series_run_list = fetch_handler.get_series_run_list(constants.SECONDARY_SERIES, FORCE_FETCH)
    
    print(f'main series run list is size {len(main_series_run_list)}')    
    print(f'secondary series run list is size {len(secondary_series_run_list)}')
