from common import constants
from pathlib import Path
import json

import pandas as pd


REFERENCE_DIRECTORY = 'reference'
LEADERBOARD_DIRECTORY = 'dumps/leaderboard'

SERIES_INFO_DIRECTORY = 'dumps/series_info'
CATEGORY_DIRECTORY = 'dumps/category_info'
GAME_DIRECTORY = 'dumps/game_info'

SERIES_RUN_LIST_DIRECTORY = 'dumps/series_run_list'
GAME_RUN_LIST_DIRECTORY = 'dumps/game_run_list'
CATEGORY_RUN_LIST_DIRECTORY = 'dumps/category_run_list'
USER_RUN_LIST_DIRECTORY = 'dumps/user_run_list'


def load_json(path):
    path = Path(str(path))

    if path.exists():
        with path.open('r') as file:
            return json.load(file)
    else:
        return {}


def dump_json(data, path):
    path = Path(str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=4))


def make_text_file(text, file_name):
    path = Path(file_name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def make_csv_file_from_data_frame(df, path, index=False):
    path = Path(str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(str(path), index=index)


def make_single_sort_csv(df, path, sort_id, sort_name, ref, add_empties=False):
    counts = (
        df
        .groupby([sort_id])
        .size()
    )

    if add_empties:
        counts = counts.reindex(ref.keys(), fill_value=0)

    out = (
        counts
        .rename('count')
        .reset_index()
    )

    out[sort_name] = out[sort_id].map(ref)

    out = (
        out
        [[sort_name, 'count']]
        .sort_values(by=['count', sort_name], ascending=[False, True])
    )

    out.to_csv(path, index=False)

def make_double_sort_csv(df, path, sort1_id, sort2_id, sort1_name, sort2_name, ref1, ref2, all_pairs):
    counts = df.groupby([sort1_id, sort2_id]).size()

    full_index = pd.MultiIndex.from_tuples(all_pairs, names=[sort1_id, sort2_id])
    counts = counts.reindex(full_index, fill_value=0)

    out = counts.reset_index(name='count')


    out[sort1_name] = out[sort1_id].map(ref1)
    out[sort2_name] = out[sort2_id].map(ref2)

    out = (
        out
        [[sort1_name, sort2_name, 'count']]
        .sort_values(by=['count', sort1_name, sort2_name], ascending=[False, True, True])
    )

    out.to_csv(path, index=False)


# region get file paths
def get_series_run_list_path(game_id):
    return Path(f'{SERIES_RUN_LIST_DIRECTORY}/{game_id}_series_run_list.json')


def get_game_run_list_path(game_id):
    return Path(f'{GAME_RUN_LIST_DIRECTORY}/{game_id}_game_run_list.json')


def get_category_run_list_path(category_id):
    return Path(f'{CATEGORY_RUN_LIST_DIRECTORY}/{category_id}_category_run_list.json')


def get_user_run_list_path(user_id):
    return Path(f'{USER_RUN_LIST_DIRECTORY}/{user_id}_user_run_list.json')


def get_series_game_info_list_path(series_id):
    return Path(f'{SERIES_INFO_DIRECTORY}/{series_id}_series_game_info_list.json')


def get_leaderboard_path(category_id):
    return Path(f'{LEADERBOARD_DIRECTORY}/{category_id}_leaderboard.json')


def get_series_info_path(series_id):
    return Path(f'{SERIES_INFO_DIRECTORY}/{series_id}_series_info')


def get_category_info_path(category_id):
    return Path(f'{CATEGORY_DIRECTORY}/{category_id}_category_info.json')


def get_game_info_path(game_id):
    return Path(f'{GAME_DIRECTORY}/{game_id}_game_info.json')
# endregion
