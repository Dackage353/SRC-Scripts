from common import fetch_handler, file_helper, reference, src_helper, tool
from classes import CategoryInfo, GameInfo, RunInfo


FORCE_FETCH = False

runs = []


def process_category_run_list(category_id):    
    data = fetch_handler.fetch_category_run_list_data(category_id)

    for run_data in data:
        run = RunInfo(run_data)
        runs.append(run)
        
    
if __name__ == '__main__':
    categories = fetch_handler.fetch_all_fullgame_categories(FORCE_FETCH)

    for category in categories:
        process_category_run_list(category.id)
        print(f'processed run list for {category.get_game_name()} - {category.name}')


    df = tool.get_data_frame_for_run_list(runs)

    file_name = 'all_runs'
    file_helper.make_csv_file_from_data_frame(df, f'output/{file_name}.csv')

    file_helper.make_single_sort_csv(df, f'output/{file_name} - runs per game.txt', 'game_id', 'game_name', reference.game_names, True)
    file_helper.make_single_sort_csv(df, f'output/{file_name} - runs per player.txt', 'single_player_id', 'single_player_name', reference.user_names, True)
    file_helper.make_single_sort_csv(df, f'output/{file_name} - runs per verifier.txt', 'verifier_id', 'verifier_name', reference.user_names, False)
    
    all_pairs = [(category.game_id, category.id) for category in categories]
    file_helper.make_double_sort_csv(df, f'output/{file_name} - runs per category.csv', 'game_id', 'category_id', 'game_name', 'category_name', reference.game_names, reference.category_names, all_pairs)


    