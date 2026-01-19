from common import file_helper, reference, src_helper, tool, constants
from pathlib import Path

# names

def fetch_game_name(game_id):
    if game_id:
        if game_id not in reference.game_names:
            data = src_helper.request_src(src_helper.get_game_url(game_id)).get('data')
            name = data.get('names', {}).get('international')
            reference.game_names[game_id] = name
            print(f'fetched name for {game_id} - {name}')

        return reference.game_names[game_id]


def fetch_category_name(category_id, data=None):
    if category_id:
        if category_id not in reference.category_names:
            if data is None:
                data = src_helper.request_src(src_helper.get_category_url(category_id)).get('data')
                name = data.get('name')
                print(f'fetched name for {category_id} - {name}')

            reference.category_names[category_id] = data.get('name')
            
        return reference.category_names[category_id]


def fetch_user_name(user_id):
    if user_id:
        if user_id not in reference.user_names:
            request = src_helper.request_src_no_error(src_helper.get_user_url(user_id))

            if request:
                data = request.get('data')
                name = data.get('names', {}).get('international')
                reference.user_names[user_id] = name
                print(f'fetched name for {user_id} - {name}')
            else:
                reference.user_names[user_id] = ""
                print(f'fetched user id was missing - {user_id}')

        return reference.user_names[user_id]


def fetch_series_game_names(force_fetch=False, series_id=constants.MAIN_SERIES):
    data = fetch_series_info(force_fetch, series_id)
    games = tool.create_game_info_from_data(data)

    return [game.name_international for game in games]


# info


def fetch_game_info(game_ids, force_fetch=False):
    series = fetch_series_info(force_fetch)

    return [
        game for game in series
        if game['id'] in game_ids
    ]


def fetch_category_info(category_id, force_fetch=False):
    path = Path(f'{constants.CATEGORY_DIRECTORY}/{category_id}.json')

    if not force_fetch and path.exists():
        return file_helper.load_json(path)
    else:
        data = src_helper.request_src(src_helper.get_category_url(category_id)).get('data')
        fetch_category_name(category_id, data)
        print(f'fetched category data for {category_id} - {reference.category_names[category_id]}')

        file_helper.dump_json(data, path)
        return data

def fetch_series_info(force_fetch=False, series_id=constants.MAIN_SERIES):
    path = Path(f'{constants.SERIES_INFO_DIRECTORY}/{series_id}_series_info')
        
    if not force_fetch and path.exists():
        return file_helper.load_json(path)
    else:
        link = src_helper.get_series_info_url(series_id)
        data = src_helper.request_src_list(link)

        reference.add_info_from_game_data_list(data)
        file_helper.dump_json(data, path)
        print(f'fetched game list of size {len(data)}')
        return data
    

# leaderboards


def fetch_category_leaderboards(category_ids, force_fetch=False):
    for category_id in category_ids:
        fetch_leaderboard(category_id, force_fetch)


def fetch_leaderboard(category_id, force_fetch=False):
    path = Path(f'{constants.LEADERBOARD_DIRECTORY}/{category_id}.json')
    
    if not force_fetch and path.exists():
        return file_helper.load_json(path)
    else:
        category_data = fetch_category_info(category_id, False)

        leaderboard_link = None
        for link in category_data.get('links'):
            if link.get('rel') == 'leaderboard':
                leaderboard_link = link.get('uri')
                break

        if leaderboard_link:
            data = src_helper.request_src(leaderboard_link).get('data')
            file_helper.dump_json(data, path)
            
            print(f'fetched leaderboard data for {category_id} - {reference.category_names[category_id]}')
            return data
        else:
            return None


# category lists


def fetch_all_fullgame_categories(force_fetch=False, series_id=constants.MAIN_SERIES):
    data = fetch_series_info(force_fetch, series_id)
    fullgame_categories = []

    for game in data:
        categories_data = game.get('categories', {}).get('data')

        categories = tool.create_category_info_from_data(categories_data)
        fullgame_categories.extend([category for category in categories if category.type == 'per-game'])

    return fullgame_categories


# get lists


def get_series_game_info_list(series_id, force_fetch=False):
    path = get_series_game_info_list_path(series_id)
    if not force_fetch and path.exists():
        data = file_helper.load_json(path)

    else:
        data = fetch_series_game_info_list(series_id)

    return tool.create_game_info_from_data(data)


def get_series_run_list(series_id, force_fetch=False):
    path = get_series_run_list_path(series_id)
    data = []

    if not force_fetch and path.exists():
        data = file_helper.load_json(path)

    else:
        games = get_series_game_info_list(series_id, force_fetch)
        for game in games:
            data.extend(fetch_game_run_list_data(game.id))

        file_helper.dump_json(data, path)

    return tool.create_run_info_from_data(data)


def get_game_run_list(game_id, force_fetch=False):
    path = get_game_run_list_path(game_id)

    if not force_fetch and path.exists():
        data = file_helper.load_json(path)

    else:
        data = fetch_category_run_list_data(game_id)

    return tool.create_run_info_from_data(data)


def get_category_run_list(category_id, force_fetch=False):
    path = get_category_run_list_path(category_id)

    if not force_fetch and path.exists():
        data = file_helper.load_json(path)

    else:
        data = fetch_category_run_list_data(category_id)

    return tool.create_run_info_from_data(data)


def get_user_run_list(user_id, force_fetch=False):
    path = get_user_run_list_path(user_id)

    if not force_fetch and path.exists():
        data = file_helper.load_json(path)

    else:
        data = fetch_user_run_list_data(user_id)

    return tool.create_run_info_from_data(data)


# fetch run list data


def fetch_game_run_list_data(game_id):
    path = get_game_run_list_path(game_id)

    game_name = fetch_game_name(game_id)
    print(f'starting to fetch game {game_id}:{game_name} run list')

    link = src_helper.get_game_run_list_url(game_id)
    data = src_helper.request_src_list(link)
    file_helper.dump_json(data, path)
    
    print(f'fetched game {game_id}:{game_name} run list of size {len(data)}')
    return data


def fetch_category_run_list_data(category_id):
    path = get_category_run_list_path(category_id)

    category_name = fetch_category_name(category_id)
    print(f'starting to fetch category {category_id}:{category_name} run list')

    link = src_helper.get_category_run_list_url(category_id)
    data = src_helper.request_src_list(link)
    file_helper.dump_json(data, path)
    
    print(f'fetched category {category_id}:{category_name} run list of size {len(data)}')
    return data


def fetch_user_run_list_data(user_id):
    path = get_user_run_list_path(user_id)

    user_name = fetch_user_name(user_id)
    print(f'starting to fetch user {user_id}:{user_name} run list')

    link = src_helper.get_runs_by_user_url(user_id)
    data = src_helper.request_src_list(link)
    file_helper.dump_json(data, path)
    
    print(f'fetched user {user_id}:{user_name} run list of size {len(data)}')
    return data


# directory paths


def get_series_run_list_path(game_id):
    return Path(f'{constants.SERIES_RUN_LIST_DIRECTORY}/{game_id}_series_run_list.json')


def get_game_run_list_path(game_id):
    return Path(f'{constants.GAME_RUN_LIST_DIRECTORY}/{game_id}_game_run_list.json')


def get_category_run_list_path(category_id):
    return Path(f'{constants.CATEGORY_RUN_LIST_DIRECTORY}/{category_id}_category_run_list.json')


def get_user_run_list_path(user_id):
    return Path(f'{constants.USER_RUN_LIST_DIRECTORY}/{user_id}_user_run_list.json')


def get_series_game_info_list_path(series_id):
    return Path(f'{constants.SERIES_INFO_DIRECTORY}/{series_id}_series_game_info_list.json')


# unsorted


def fetch_series_game_info_list(series_id):
    path = get_series_game_info_list_path(series_id)

    print(f'starting to fetch series {series_id} game info list')

    link = src_helper.get_series_game_info_list_url(series_id)
    data = src_helper.request_src_list(link)
    file_helper.dump_json(data, path)

    print(f'fetched series {series_id} game info list of size {len(data)}')
    return data


def fetch_all_fullgame_category_run_lists(force_fetch=False):
    run_lists = []

    for category_id in reference.category_names:
        run_list = fetch_category_run_list(category_id, force_fetch)
        run_lists.append(run_list)

    return run_lists


def fetch_category_run_lists(category_ids, force_fetch=False):
    run_lists = []

    for category_id in category_ids:
        run_list = fetch_category_run_list(category_id, force_fetch)
        run_lists.append(run_list)

    return run_lists


def fetch_category_run_list(category_id, force_fetch=False, make_csv=False):
    data = fetch_category_run_list_data(category_id, force_fetch)
    runs = tool.create_run_info_from_data(data)

    if make_csv:
        df = tool.get_data_frame_for_run_list(runs)
        file_helper.make_csv_file_from_data_frame(df, f'output/run-list_{category_id}.csv')

    return runs
