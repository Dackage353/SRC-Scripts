from common import fetch_handler, file_helper, reference, src_helper, tool, constants
import time


script_start = time.perf_counter()

FORCE_FETCH = False
        
    
if __name__ == '__main__':
    runs = fetch_handler.get_series_run_list(constants.MAIN_SERIES, FORCE_FETCH)
    runs.extend(fetch_handler.get_series_run_list(constants.SECONDARY_SERIES, FORCE_FETCH))

    df = tool.get_data_frame_for_run_list(runs)

    file_name = 'all_runs'
    file_helper.make_csv_file_from_data_frame(df, f'output/{file_name}.csv')

    file_helper.make_single_sort_csv(df, f'output/{file_name} - runs per game.csv', 'game_id', 'game_name', reference.game_names, True)
    file_helper.make_single_sort_csv(df, f'output/{file_name} - runs per player.csv', 'solo_player_id', 'solo_player_name', reference.user_names, True)
    file_helper.make_single_sort_csv(df, f'output/{file_name} - runs per verifier.csv', 'verifier_id', 'verifier_name', reference.user_names, False)
    
    #all_pairs = [(category.game_id, category.id) for category in categories]
    #file_helper.make_double_sort_csv(df, f'output/{file_name} - runs per category.csv', 'game_id', 'category_id', 'game_name', 'category_name', reference.game_names, reference.category_names, all_pairs)
    
    script_end = time.perf_counter()
    print(f"\nElapsed time: {script_end - script_start:.2f} seconds")
