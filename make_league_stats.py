from datetime import datetime, timezone
from pathlib import Path
import src_helper
import json
import pandas as pd
import data_classes
import file_handler

runs = []
valid_runs = []
invalid_runs = []

category_ids = [
    '7dg6eqlk',
    'wkp3l782',
    'vdo1vj92',
    '7kje1wnd',
    'xk94874d',
    'z27qlj0k',
    'rkl3w36k',
    '9kv9zv82',
    'zd3xe9vd'
]

start_time = datetime(2025, 10, 4, 4, 35, tzinfo=timezone.utc)
end_time = datetime(2025, 12, 1, 11, 0, tzinfo=timezone.utc)
    

def process_category_run_list(category_id):    
    data = file_handler.fetch_category_run_list(category_id)

    for run_data in data:
        run = data_classes.Run.create_from_json(run_data)
        
        runs.append(run)
        if start_time <= run.time_submitted <= end_time and run.verified_status == 'verified':
            valid_runs.append(run)
        else:
            invalid_runs.append(run)
    
    
def fetch_missing_names():
    for run in runs:
        file_handler.check_game_name(run.game_id)
        file_handler.check_category_name(run.category_id)
        file_handler.check_player_name(run.player_id)
        file_handler.check_player_name(run.verifier_id)

    
def make_files_for_runs(runs, file_name):
    df = get_data_frame_for_runs(runs)
    
    csv_path = Path(f'output/{file_name}.csv')
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(str(csv_path), index=False)
    
    file_handler.make_text_file(df.groupby('game_name').size().to_string(header=False), f'output/{file_name} - runs per game.txt')
    file_handler.make_text_file(df.groupby('category_name').size().to_string(header=False), f'output/{file_name} - runs per category.txt')
    file_handler.make_text_file(df.groupby('player_name').size().to_string(header=False), f'output/{file_name} - runs per player.txt')
    file_handler.make_text_file(df.groupby('verifier_name').size().to_string(header=False), f'output/{file_name} - runs per verifier.txt')

    
def get_data_frame_for_runs(runs):
    run_dicts = [vars(run) for run in runs]
    df = pd.DataFrame(run_dicts)
    
    df['game_name'] = df['game_id'].map(file_handler.game_names)
    df['category_name'] = df['category_id'].map(file_handler.category_names)
    df['player_name'] = df['player_id'].map(file_handler.player_names)
    df['verifier_name'] = df['verifier_id'].map(file_handler.player_names)
    
    df = df.sort_values(['game_name', 'category_name', 'player_name'], ascending=[True, True, True])
    
    return df
    
    
if __name__ == '__main__':    
    for category_id in category_ids:
        process_category_run_list(category_id)

    fetch_missing_names()
    
    make_files_for_runs(valid_runs, 'valid_runs')
    make_files_for_runs(invalid_runs, 'invalid_runs')
    make_files_for_runs(runs, 'runs')
    