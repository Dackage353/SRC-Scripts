import src_helper
import json
import atexit
from pathlib import Path

CATEGORY_DIRECTORY = 'category_dump'
LEADERBOARD_DIRECTORY = 'leaderboard_dump'
CATEGORY_RUN_LIST_DIRECTORY = 'category_run_list_dump'
REFERENCE_DIRECTORY = 'reference'

def load_names(file_name):
    path = Path(f'{REFERENCE_DIRECTORY}/{file_name}')
    
    if path.exists():
        with path.open('r') as file:
            return json.load(file)
    
    return {}

def load_json(path):
    with path.open('r') as file:
        return json.load(file)


def dump_json(data, path):
    path = Path(str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=4))


def make_text_file(text, file_name):
    path = Path(file_name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    

def check_game_name(game_id):
    if game_id not in game_names:
        data = src_helper.request_src(src_helper.get_game(game_id))['data']
        name = data['names']['international']
        game_names[game_id] = name
        print(f'fetched name for {game_id} - {name}')


def check_category_name(category_id, data=None):
    if category_id not in category_names:
        if data is None:
            data = src_helper.request_src(src_helper.get_category(category_id))['data']
            name = data['name']
            print(f'fetched name for {category_id} - {name}')

        category_names[category_id] = data['name']


def check_player_name(player_id):
    if player_id not in player_names:
        data = src_helper.request_src(src_helper.get_user(player_id))['data']
        name = data['names']['international']
        player_names[player_id] = name
        print(f'fetched name for {player_id} - {name}')


def save_reference_names():
    sorted_game_names = dict(sorted(game_names.items(), key=lambda item: item[1]))
    sorted_category_names = dict(sorted(category_names.items(), key=lambda item: item[1]))
    sorted_player_names = dict(sorted(player_names.items(), key=lambda item: item[1]))
    
    dump_json(sorted_game_names, f'{REFERENCE_DIRECTORY}/game_names.json')
    dump_json(sorted_category_names, f'{REFERENCE_DIRECTORY}/category_names.json')
    dump_json(sorted_player_names, f'{REFERENCE_DIRECTORY}/player_names.json')


def fetch_category_data(category_id):
    path = Path(f'{CATEGORY_DIRECTORY}/{category_id}.json')
    
    if path.exists():
        return load_json(path)
    else:
        data = src_helper.request_src(src_helper.get_category(category_id))['data']
        check_category_name(category_id, data)
        print(f'fetched category data for {category_id} - {category_names[category_id]}')

        dump_json(data, path)
        return data


def fetch_leaderboard_data(category_id):
    path = Path(f'{LEADERBOARD_DIRECTORY}/{category_id}.json')
    
    if path.exists():
        return load_json(path)
    else:
        category_data = fetch_category_data(category_id)

        leaderboard_link = None
        for link in category_data['links']:
            if link['rel'] == 'leaderboard':
                leaderboard_link = link['uri']
                break

        data = src_helper.request_src(leaderboard_link)['data']
        print(f'fetched leaderboard data for {category_id} - {category_names[category_id]}')
        dump_json(data, path)
        return data

def fetch_category_run_list(category_id):
    path = Path(f'{CATEGORY_RUN_LIST_DIRECTORY}/{category_id}.json')

    if path.exists():
        return load_json(path)
    else:
        data = src_helper.request_src(src_helper.get_category_run_list(category_id))['data']
        check_category_name(category_id)
        print(f'fetched category run list for {category_id} - {category_names[category_id]}')

        dump_json(data, path)
        return data

game_names = load_names('game_names.json')
category_names = load_names('category_names.json')
player_names = load_names('player_names.json')

atexit.register(save_reference_names)