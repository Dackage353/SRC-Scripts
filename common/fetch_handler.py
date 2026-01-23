from common import file_helper, reference, src_helper, tool, constants


# region get names
def get_game_name(game_id: str, force_fetch: bool = False):
    if game_id:
        if force_fetch or game_id not in reference.game_names:
            link = src_helper.get_game_url(game_id)
            request = src_helper.request_src_no_error(link)

            if request:
                data = request.get('data')
                name = data.get('names', {}).get('international')
                reference.game_names[game_id] = name
                print(f'fetched name for {game_id}:{name}')

            else:
                reference.game_names[game_id] = ""
                print(f'fetched game id {game_id} was missing')

        return reference.game_names[game_id]


def get_category_name(category_id: str, force_fetch: bool = False):
    if category_id:
        if force_fetch or category_id not in reference.category_names:
            link = src_helper.get_category_url(category_id)
            request = src_helper.request_src_no_error(link)

            if request:
                data = request.get('data')
                name = data.get('name')
                reference.category_names[category_id] = name
                print(f'fetched name for {category_id}:{name}')

            else:
                reference.category_names[category_id] = ""
                print(f'fetched category id {category_id} was missing')
        
        return reference.category_names[category_id]


def get_user_name(user_id: str, force_fetch: bool = False):
    if user_id:
        if force_fetch or user_id not in reference.user_names:
            link = src_helper.get_user_url(user_id)
            request = src_helper.request_src_no_error(link)

            if request:
                data = request.get('data')
                name = data.get('names', {}).get('international')
                reference.user_names[user_id] = name
                print(f'fetched name for {user_id}:{name}')

            else:
                reference.user_names[user_id] = ""
                print(f'fetched user id {user_id} was missing')
        
        return reference.user_names[user_id]
    
    
def get_series_game_names(series_id: str, force_fetch: bool = False):
    data = get_series_info(series_id, force_fetch)
    games = tool.create_game_info_from_data(data)

    return [game.name_international for game in games]
# endregion

# region get run lists
def get_series_run_list(series_id, force_fetch=False):
    path = file_helper.get_series_run_list_path(series_id)
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
    path = file_helper.get_game_run_list_path(game_id)

    if not force_fetch and path.exists():
        data = file_helper.load_json(path)

    else:
        data = fetch_category_run_list_data(game_id)

    return tool.create_run_info_from_data(data)


def get_category_run_list(category_id, force_fetch=False):
    path = file_helper.get_category_run_list_path(category_id)

    if not force_fetch and path.exists():
        data = file_helper.load_json(path)

    else:
        data = fetch_category_run_list_data(category_id)

    return tool.create_run_info_from_data(data)


def get_user_run_list(user_id, force_fetch=False):
    path = file_helper.get_user_run_list_path(user_id)

    if not force_fetch and path.exists():
        data = file_helper.load_json(path)

    else:
        data = fetch_user_run_list_data(user_id)

    return tool.create_run_info_from_data(data)
# endregion


# region get basic info
def get_series_game_info_list(series_id, force_fetch=False):
    path = file_helper.get_series_game_info_list_path(series_id)
    if not force_fetch and path.exists():
        data = file_helper.load_json(path)

    else:
        data = fetch_series_game_info_list(series_id)

    return tool.create_game_info_from_data(data)
# endregion


# region fetch basic info
def get_series_info(series_id: str, force_fetch: bool = False):
    path = file_helper.get_series_info_path(series_id)
        
    if not force_fetch and path.exists():
        return file_helper.load_json(path)
    
    else:
        print(f'starting to fetch series data for {series_id}')
        link = src_helper.get_series_info_url(series_id)
        data = src_helper.request_src_list(link)
        print(f'fetched series data for {series_id}')

        reference.add_info_from_game_data_list(data)
        file_helper.dump_json(data, path)
        return data


def get_category_info(category_id, force_fetch=False):
    path = file_helper.get_category_info_path(category_id)

    if not force_fetch and path.exists():
        return file_helper.load_json(path)
    
    else:
        print(f'starting to fetch category data for {category_id}')
        link = src_helper.get_category_url(category_id)
        data = src_helper.request_src(link).get('data')
        name = get_category_name(category_id)
        print(f'fetched category data for {category_id}:{name}')

        file_helper.dump_json(data, path)
        return data


def fetch_game_info(game_id, force_fetch=False):
    path = file_helper.get_game_info_path(game_id)

    if not force_fetch and path.exists():
        return file_helper.load_json(path)
    
    else:
        print(f'starting to fetch game data for {game_id}')
        link = src_helper.get_game_url(game_id)
        data = src_helper.request_src(link).get('data')
        name = get_game_name(game_id)
        print(f'fetched game data for {game_id}:{name}')

        file_helper.dump_json(data, path)
        return data


def fetch_series_game_info_list(series_id):
    path = file_helper.get_series_game_info_list_path(series_id)

    print(f'starting to fetch series {series_id} game info list')
    link = src_helper.get_series_game_info_list_url(series_id)
    data = src_helper.request_src_list(link)
    print(f'fetched series {series_id} game info list of size {len(data)}')

    file_helper.dump_json(data, path)
    return data
# endregion


# region fetch run list data
def fetch_game_run_list_data(game_id):
    path = file_helper.get_game_run_list_path(game_id)

    game_name = get_game_name(game_id)
    print(f'starting to fetch game {game_id}:{game_name} run list')

    link = src_helper.get_game_run_list_url(game_id)
    data = src_helper.request_src_list(link)
    file_helper.dump_json(data, path)
    
    print(f'fetched game {game_id}:{game_name} run list of size {len(data)}')
    return data


def fetch_category_run_list_data(category_id):
    path = file_helper.get_category_run_list_path(category_id)

    category_name = get_category_name(category_id)
    print(f'starting to fetch category {category_id}:{category_name} run list')

    link = src_helper.get_category_run_list_url(category_id)
    data = src_helper.request_src_list(link)
    file_helper.dump_json(data, path)
    
    print(f'fetched category {category_id}:{category_name} run list of size {len(data)}')
    return data


def fetch_user_run_list_data(user_id):
    path = file_helper.get_user_run_list_path(user_id)

    user_name = get_user_name(user_id)
    print(f'starting to fetch user {user_id}:{user_name} run list')

    link = src_helper.get_user_run_list_url(user_id)
    data = src_helper.request_src_list(link)
    file_helper.dump_json(data, path)
    
    print(f'fetched user {user_id}:{user_name} run list of size {len(data)}')
    return data
# endregion


# region leaderboards
def get_leaderboard(category_id: str, force_fetch: bool = False):
    path = file_helper.get_leaderboard_path(category_id)
    
    if not force_fetch and path.exists():
        return file_helper.load_json(path)
    else:
        return fetch_leaderboard(category_id)


def fetch_leaderboard(category_id: str):
    path = file_helper.get_leaderboard_path(category_id)
    
    print(f'starting to fetch category {category_id} leaderboard')
    category_data = get_category_info(category_id, False)
    print(f'fetched category {category_id} leaderboard')

    leaderboard_link = None
    for link in category_data.get('links'):
        if link.get('rel') == 'leaderboard':
            leaderboard_link = link.get('uri')
            break

    if leaderboard_link:
        data = src_helper.request_src(leaderboard_link).get('data')
        file_helper.dump_json(data, path)
        
        
        return data
    else:
        return None
# endregion


# region category lists
def get_all_fullgame_categories(series_id: str, force_fetch: bool = False):
    data = get_series_info(series_id, force_fetch)
    fullgame_categories = []

    for game in data:
        categories_data = game.get('categories', {}).get('data')

        categories = tool.create_category_info_from_data(categories_data)
        fullgame_categories.extend([category for category in categories if category.type == 'per-game'])

    return fullgame_categories
# endregion
