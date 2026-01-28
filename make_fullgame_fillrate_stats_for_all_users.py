import pandas as pd
from common import fetch_handler, file_helper, reference, src_helper, tool, constants


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
    runs = fetch_handler.get_series_run_list(constants.MAIN_SERIES, FORCE_FETCH)
    runs.extend(fetch_handler.get_series_run_list(constants.SECONDARY_SERIES, FORCE_FETCH))

    tool.check_for_missing_names_in_run_list(runs)
    runs_by_category = tool.sort_runs_by_category_id(runs)

    fullgame_categories = fetch_handler.get_all_fullgame_categories(constants.MAIN_SERIES, FORCE_FETCH)
    fullgame_categories.extend(fetch_handler.get_all_fullgame_categories(constants.SECONDARY_SERIES, FORCE_FETCH))


    fullgame_set_per_user = {user_id: set() for user_id in reference.user_names}

    for fullgame_category in fullgame_categories:
        category_runs = runs_by_category.get(fullgame_category.id, [])

        for run in category_runs:
            for player_id in run.get_player_ids():
                fullgame_set_per_user[player_id].add(fullgame_category.id)

        print(f'finished category {fullgame_category.id}:{fullgame_category.game_and_category_name}')


    make_csv_for_fullgame_fill_counts(fullgame_set_per_user)
