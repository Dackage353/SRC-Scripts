from common import file_helper, reference, src_helper, tool, constants
from pathlib import Path


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


def fetch_series_game_names(force_fetch=False, series=constants.DEFAULT_SERIES):
    data = fetch_series_info(force_fetch, series)
    games = tool.create_game_info_from_data(data)

    return [game.name_international for game in games]


def fetch_series_info(force_fetch=False, series=constants.DEFAULT_SERIES):
    path = Path(f'{constants.SERIES_INFO_DIRECTORY}/{series}_series_info')
        
    if not force_fetch and path.exists():
        return file_helper.load_json(path)
    else:
        link = src_helper.get_series_info_url(series)
        data = src_helper.request_src_list(link)

        reference.add_info_from_game_data_list(data)
        file_helper.dump_json(data, path)
        print(f'fetched game list of size {len(data)}')
        return data


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


def fetch_category_run_lists(category_ids, force_fetch=False):
    for category_id in category_ids:
        data = fetch_category_run_list_data(category_id, force_fetch)
        runs = tool.create_run_info_from_data(data)

        df = tool.get_data_frame_for_run_list(runs)
        file_helper.make_csv_file_from_data_frame(df, f'output/run-list_{category_id}.csv')


def fetch_category_run_list_data(category_id, force_fetch=False):
    path = Path(f'{constants.CATEGORY_RUN_LIST_DIRECTORY}/{category_id}.json')

    if not force_fetch and path.exists():
        return file_helper.load_json(path)
    else:
        data = src_helper.request_src_list(src_helper.get_category_run_list_url(category_id))

        fetch_category_name(category_id)
        file_helper.dump_json(data, path)
        
        print(f'fetched category run list for {category_id} - {reference.category_names[category_id]}')
        return data


def fetch_all_fullgame_categories(force_fetch=False):
    data = fetch_series_info(force_fetch)
    fullgame_categories = []

    for game in data:
        categories_data = game.get('categories', {}).get('data')

        categories = tool.create_category_info_from_data(categories_data)
        fullgame_categories.extend([category for category in categories if category.type == 'per-game'])

    return fullgame_categories


    