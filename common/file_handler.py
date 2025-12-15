from pathlib import Path
import atexit
import common.src_helper as src_helper
import json
import pandas as pd

CATEGORY_DIRECTORY = 'category_info_dump'
LEADERBOARD_DIRECTORY = 'leaderboard_dump'
CATEGORY_RUN_LIST_DIRECTORY = 'category_run_list_dump'
REFERENCE_DIRECTORY = 'reference'
ROM_HACK_LIST_DIRECTORY = 'dump'

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
    

def check_for_missing_info_from_runs(runs):
    for run in runs:
        fetch_game_name(run.game_id)
        fetch_category_name(run.category_id)
        fetch_user_name(run.player_id)
        fetch_user_name(run.verifier_id)


def fetch_game_name(game_id):
    if game_id:
        if game_id not in game_names:
            data = src_helper.request_src(src_helper.get_game_url(game_id))['data']
            name = data['names']['international']
            game_names[game_id] = name
            print(f'fetched name for {game_id} - {name}')

        return game_names[game_id]


def fetch_category_name(category_id, data=None):
    if category_id:
        if category_id not in category_names:
            if data is None:
                data = src_helper.request_src(src_helper.get_category_url(category_id))['data']
                name = data['name']
                print(f'fetched name for {category_id} - {name}')

            name = data['name']
            category_names[category_id] = name
            
        return category_names[category_id]


def fetch_user_name(user_id):
    if user_id:
        if user_id not in user_names:
            request = src_helper.request_src_no_error(src_helper.get_user_url(user_id))

            if request:
                data = request['data']
                name = data['names']['international']
                user_names[user_id] = name
                print(f'fetched name for {user_id} - {name}')
            else:
                user_names[user_id] = ""
                print(f'fetched user id was missing - {user_id}')

        return user_names[user_id] 


def save_reference_names():
    sorted_game_names = dict(sorted(game_names.items(), key=lambda item: item[1]))
    sorted_category_names = dict(sorted(category_names.items(), key=lambda item: item[1]))
    sorted_level_names = dict(sorted(level_names.items(), key=lambda item: item[1]))
    sorted_user_names = dict(sorted(user_names.items(), key=lambda item: item[1]))
    
    dump_json(sorted_game_names, f'{REFERENCE_DIRECTORY}/game_names.json')
    dump_json(sorted_category_names, f'{REFERENCE_DIRECTORY}/category_names.json')
    dump_json(sorted_level_names, f'{REFERENCE_DIRECTORY}/level_names.json')
    dump_json(sorted_user_names, f'{REFERENCE_DIRECTORY}/user_names.json')


def fetch_category_info(category_id):
    path = Path(f'{CATEGORY_DIRECTORY}/{category_id}.json')
    
    if path.exists():
        return load_json(path)
    else:
        data = src_helper.request_src(src_helper.get_category_url(category_id))['data']
        fetch_category_name(category_id, data)
        print(f'fetched category data for {category_id} - {category_names[category_id]}')

        dump_json(data, path)
        return data


def fetch_leaderboard(category_id):
    path = Path(f'{LEADERBOARD_DIRECTORY}/{category_id}.json')
    
    if path.exists():
        return load_json(path)
    else:
        category_data = fetch_category_info(category_id)

        leaderboard_link = None
        for link in category_data['links']:
            if link['rel'] == 'leaderboard':
                leaderboard_link = link['uri']
                break

        data = src_helper.request_src_list(leaderboard_link)['data']
        dump_json(data, path)
        
        print(f'fetched leaderboard data for {category_id} - {category_names[category_id]}')
        return data


def fetch_category_run_list(category_id):
    path = Path(f'{CATEGORY_RUN_LIST_DIRECTORY}/{category_id}.json')

    if path.exists():
        return load_json(path)
    else:
        data = src_helper.request_src_list(src_helper.get_category_run_list_url(category_id))

        fetch_category_name(category_id)
        dump_json(data, path)
        
        print(f'fetched category run list for {category_id} - {category_names[category_id]}')
        return data


def fetch_rom_hack_info_list():
    path = Path(f'{ROM_HACK_LIST_DIRECTORY}/rom_hacks.json')
        
    if path.exists():
        return load_json(path)
    else:
        link = src_helper.get_detailed_rom_hacks_url()
        data = src_helper.request_src_list(link)

        add_info_from_game_data_list(data)
        dump_json(data, path)
        print(f'fetched rom hack list of size {len(data)}')
        return data


def add_info_from_game_data_list(data):
    global game_names, category_names, level_names

    for game in data:
        game_names[game['id']] = game['names']['international']

        for category in game['categories']['data']:
            category_names[category['id']] = category['name']
            
        for level in game['levels']['data']:
            level_names[level['id']] = level['name']


def get_data_frame_for_run_list(runs):
    check_for_missing_info_from_runs(runs)
    df = pd.DataFrame(runs)
    
    df['game_name'] = df['game_id'].map(game_names)
    df['category_name'] = df['category_id'].map(category_names)
    df['player_name'] = df['player_id'].map(user_names)
    df['verifier_name'] = df['verifier_id'].map(user_names)
    
    df = df.sort_values(['game_name', 'category_name', 'player_name'], ascending=[True, True, True])
    
    return df


def make_csv_file_from_data_frame(df, path):
    path = Path(str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(str(path), index=False)


game_names = load_names('game_names.json')
category_names = load_names('category_names.json')
level_names = load_names('level_names.json')
user_names = load_names('user_names.json')

atexit.register(save_reference_names)
