from datetime import datetime, timezone
import common.data_classes as data_classes
import common.file_handler as file_handler

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

    
def make_files_for_runs(runs, file_name):
    df = file_handler.get_data_frame_for_run_list(runs)

    file_handler.make_csv_file_from_data_frame(df, f'output/{file_name}.csv')
    
    file_handler.make_text_file(df.groupby('game_name').size().to_string(header=False), f'output/{file_name} - runs per game.txt')
    file_handler.make_text_file(df.groupby('category_name').size().to_string(header=False), f'output/{file_name} - runs per category.txt')
    file_handler.make_text_file(df.groupby('player_name').size().to_string(header=False), f'output/{file_name} - runs per player.txt')
    file_handler.make_text_file(df.groupby('verifier_name').size().to_string(header=False), f'output/{file_name} - runs per verifier.txt')

    
if __name__ == '__main__':    
    for category_id in category_ids:
        process_category_run_list(category_id)

    file_handler.check_for_missing_info_from_runs(runs)
    
    make_files_for_runs(valid_runs, 'valid_runs')
    make_files_for_runs(invalid_runs, 'invalid_runs')
    make_files_for_runs(runs, 'runs')
    