from classes import Game, Category, Run
from collections import defaultdict
from common import file_helper, reference, fetch_handler
from datetime import datetime, timezone
from datetime import timedelta
import pandas as pd


def sort_runs_by_category_id(runs):
    category_dict = defaultdict(list)

    for run in runs:
        category_dict[run.category_id].append(run)

    return dict(category_dict)


def check_for_missing_names_in_run_list(runs):
    for run in runs:
        for player_id in run.get_player_ids():
            fetch_handler.get_user_name(player_id)


def create_game_list_from_data(data):
    return [Game(d) for d in data]


def create_category_list_from_data(data):
    return [Category(d) for d in data]


def create_run_info_from_data(data):
    return [Run(d) for d in data]


def parse_date_and_seconds(date_and_seconds):
    if date_and_seconds is None:
        return None

    try:
        return datetime.strptime(date_and_seconds, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
    except ValueError:
        return None
    

def parse_date(date):
    if date is None:
        return None

    try:
        return datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return None


def get_formatted_time(seconds):
    td = timedelta(seconds=seconds)
    total_ms = int(td.total_seconds() * 1000)

    hours, remainder      = divmod(total_ms, 3_600_000)
    minutes, remainder    = divmod(remainder, 60_000)
    seconds, ms           = divmod(remainder, 1000)

    return f"{hours:02}:{minutes:02}:{seconds:02}.{ms:03}"


def get_data_frame_for_run_list(runs):
    reference.check_for_missing_info_from_runs(runs)
    df = pd.DataFrame([r.__dict__ for r in runs])
    
    df['game_name']             = df['game_id'].map(reference.game_names)
    df['category_name']         = df['category_id'].map(reference.category_names)
    df['solo_player_name']      = df['solo_player_id'].map(reference.user_names)
    df['verifier_name']         = df['verifier_id'].map(reference.user_names)
    
    df = df.sort_values(['game_name', 'category_name', 'solo_player_name'], ascending=[True, True, True])
    
    return df
