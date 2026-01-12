import pandas as pd
from common import fetch_handler, file_helper, reference, src_helper, tool


FORCE_FETCH = False

def make_csv_for_fullgame_fill_counts(fullgame_set_per_user):

    lengths = [(player_id, len(set)) for player_id, set in fullgame_set_per_user.items()]

    df = pd.DataFrame(
        lengths,
        columns=['player_id', 'fill_count']
    )

    df['player_name'] = df['player_id'].map(reference.user_names)
    df = df.sort_values(['fill_count', 'player_name'], ascending=[False, True])

    file_helper.make_csv_file_from_data_frame(df, 'output/player_fill_counts.csv')

if __name__ == '__main__':
    fullgame_categories = fetch_handler.fetch_all_fullgame_categories(FORCE_FETCH)
    fullgame_set_per_user = {user_id: set() for user_id in reference.user_names}

    for fullgame_category in fullgame_categories:
        run_list = fetch_handler.fetch_category_run_list(fullgame_category.id, FORCE_FETCH)

        for run in run_list:
            for player_id in run.get_player_ids():
                fullgame_set_per_user[player_id].add(fullgame_category.id)

    make_csv_for_fullgame_fill_counts(fullgame_set_per_user)
