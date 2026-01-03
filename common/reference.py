
import atexit
from common import fetch_handler, file_helper, constants


def add_info_from_game_data_list(data):
    for game in data:
        game_names[game['id']] = game['names']['international']

        for category in game['categories']['data']:
            category_names[category['id']] = category['name']
            
        for level in game['levels']['data']:
            level_names[level['id']] = level['name']


def check_for_missing_info_from_runs(runs):
    for run in runs:
        fetch_handler.fetch_game_name(run.game_id)
        fetch_handler.fetch_category_name(run.category_id)
        
        for player_id in run.get_player_ids():
            fetch_handler.fetch_user_name(player_id)

        fetch_handler.fetch_user_name(run.verifier_id)


def save_reference_names():
    sorted_game_names        = dict(sorted(game_names.items(), key=lambda item: item[1]))
    sorted_category_names    = dict(sorted(category_names.items(), key=lambda item: item[1]))
    sorted_level_names       = dict(sorted(level_names.items(), key=lambda item: item[1]))
    sorted_user_names        = dict(sorted(user_names.items(), key=lambda item: item[1]))
    
    file_helper.dump_json(sorted_game_names, f'{constants.REFERENCE_DIRECTORY}/game_names.json')
    file_helper.dump_json(sorted_category_names, f'{constants.REFERENCE_DIRECTORY}/category_names.json')
    file_helper.dump_json(sorted_level_names, f'{constants.REFERENCE_DIRECTORY}/level_names.json')
    file_helper.dump_json(sorted_user_names, f'{constants.REFERENCE_DIRECTORY}/user_names.json')


game_names        = file_helper.load_json(f'{constants.REFERENCE_DIRECTORY}/game_names.json')
category_names    = file_helper.load_json(f'{constants.REFERENCE_DIRECTORY}/category_names.json')
level_names       = file_helper.load_json(f'{constants.REFERENCE_DIRECTORY}/level_names.json')
user_names        = file_helper.load_json(f'{constants.REFERENCE_DIRECTORY}/user_names.json')

atexit.register(save_reference_names)
