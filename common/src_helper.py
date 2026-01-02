import requests
import time

_HEADERS = {
    'User-Agent': 'src-stats/1.0',
    'Accept': 'application/json',
}
_h = dict(_HEADERS)
_sleep_period = .75
_retry_sleep = 30

NON_SRC_USERS = ['Maha Maha', 'Cryogeon', 'Madghostek', 'WWMResident','atmpas','CeeSZee','255']


# basic urls
def get_runs_url():
    return 'https://www.speedrun.com/api/v1/runs'


def get_user_url(user_id):
    return f'https://www.speedrun.com/api/v1/users/{user_id}'


def get_game_url(game_id):
    return f'https://www.speedrun.com/api/v1/games/{game_id}'


def get_category_url(category_id):
    return f'https://www.speedrun.com/api/v1/categories/{category_id}'


def get_level_url(level_id):
    return f'https://www.speedrun.com/api/v1/levels/{level_id}'


def get_game_variables(game_id):
    return f'https://www.speedrun.com/api/v1/games/{game_id}/variables'


def get_category_run_list_url(category_id):
    return f'https://www.speedrun.com/api/v1/runs?category={category_id}'


def get_game_id(game):
    return f'https://www.speedrun.com/api/v1/games?name={game}'


def get_game_categories(game_id):
    return f'https://www.speedrun.com/api/v1/games/{game_id}/categories'


# complex urls
def get_leaderboard_for_game_category(game_id, category):
    return f'https://www.speedrun.com/api/v1/leaderboards/{game_id}/category/{category}?embed=players'


def get_leaderboard_for_game_level_category(game_id, level_id,category):
    return f'https://www.speedrun.com/api/v1/leaderboards/{game_id}/level/{level_id}/{category}?embed=players'


def get_series_info_url(series='0499o64v', max=200):
    return f'https://www.speedrun.com/api/v1/series/{series}/games?max={max}&embed=categories,variables,levels'


def get_games_and_categories(max=200):
    return 'https://www.speedrun.com/api/v1/games?embed=categories&max={max}'


def get_wr_for_game_category(game_id, category):
    return f'https://www.speedrun.com/api/v1/leaderboards/{game_id}/category/{category}?top=1&embed=players'


# action urls
def post_run():
    return f'https://www.speedrun.com/api/v1/runs/'


def delete_run(run_id):
    return f'https://www.speedrun.com/api/v1/runs/{run_id}'



def unverify_run(run_id):
    return f'https://www.speedrun.com/api/v1/runs/{run_id}/status'


# requests
def request_src(url):
    err_lim = 5
    err_cnt = 1
    request_finished = False
    resp = None
    # print(f'attempting to request from:{url}')
    # usually fails if we are requesting too quickly, even with the sleep, try 10 times fail if still not working
    # after 10
    while not request_finished and err_cnt <= err_lim:
        # print(f'attempt: {err_cnt}')
        try:
            resp = requests.get(url, headers=_h)
            #503 is temporary unavailable
            if resp.status_code != 503:
                request_finished = True
            err_cnt +=1
            # print('request finished')
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print(f'Error Getting Response from {url}')
            print(e)
            if err_cnt == err_lim:
                raise requests.exceptions.RequestException
            err_cnt += 1
            print(f'sleeping for {_retry_sleep} before retry')
            time.sleep(_retry_sleep)
            print('retrying')
    # probably redundant, just being careful
    if err_cnt >= err_lim:
        print(f'err_cnt greater than err_limit {err_cnt} >= {err_lim}')
        raise requests.exceptions.RequestException
    # sleep so we don't get banned by requesting too much, .1,.2 give errors after doing a few hundred
    time.sleep(_sleep_period)
    if resp is not None and (resp.status_code == 200 or resp.status_code == 201):
        return resp.json()
    elif resp.status_code != 200 and resp.status_code != 201:
        print(resp.text)
        if (resp.status_code == 400 and resp.json()[
            'message'] == 'The selected category is for individual-level runs, but no level was selected.') \
                or resp.status_code == 404:
            return resp.json()
        else:
            raise requests.exceptions.RequestException
    else:
        return None


def request_src_list(base_url):
    items = []
    max_per_request = 200

    url = base_url
    if '?' not in base_url:
        url += '?'
    url += f"&max={max_per_request}"

    while url is not None:
        response = requests.get(url, headers=_h)
        if response.status_code != 200:
            print(f"Request failed with status code {response.status_code}")
            break

        data = response.json()
        data_items = data.get("data", [])
        if not data_items:
            break
        items.extend(data_items)
        
        if 'pagination' not in data:
            break

        url = None
        for page in data['pagination']['links']:
            if page['rel'] == 'next':
                url = page['uri']
        time.sleep(_sleep_period)

    return items


def request_src_no_error(url):
    err_lim = 5
    err_cnt = 1
    request_finished = False
    resp = None

    while not request_finished and err_cnt <= err_lim:
        try:
            resp = requests.get(url, headers=_h)
            if resp.status_code != 503:
                request_finished = True
            err_cnt += 1
        except requests.exceptions.RequestException as e:
            if err_cnt == err_lim:
                break
            err_cnt += 1
            print(f'sleeping for {_retry_sleep} before retry')
            time.sleep(_retry_sleep)
            print('retrying')

    if err_cnt >= err_lim:
        print(f'err_cnt greater than err_limit {err_cnt} >= {err_lim}')
        
    time.sleep(_sleep_period)
    if resp is not None and (resp.status_code == 200 or resp.status_code == 201):
        return resp.json()
    elif resp.status_code != 200 and resp.status_code != 201:
        if (resp.status_code == 400 and resp.json()[
            'message'] == 'The selected category is for individual-level runs, but no level was selected.') \
                or resp.status_code == 404:
            return None


def post_src(url, body, api_key):
    err_lim = 5
    err_cnt = 1
    request_finished = False
    resp = None
    new_headers = _h
    new_headers['X-API-Key'] = api_key
    # print(f'attempting to request from:{url}')
    # usually fails if we are requesting too quickly, even with the sleep, try 10 times fail if still not working
    # after 10
    while not request_finished and err_cnt <= err_lim:
        # print(f'attempt: {err_cnt}')
        try:
            resp = requests.post(url, headers=new_headers, json=body)
            request_finished = True
            # print('request finished')
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print(f'Error Getting Response from {url}')
            print(e)
            if err_cnt == err_lim:
                raise requests.exceptions.RequestException
            err_cnt += 1
            print(f'sleeping for {_retry_sleep} before retry')
            time.sleep(_retry_sleep)
            print('retrying')
    # probably redundant, just being careful
    if err_cnt >= err_lim:
        print(f'err_cnt greater than err_limit {err_cnt} >= {err_lim}')
        raise requests.exceptions.RequestException
    # sleep so we don't get banned by requesting too much, .1,.2 give errors after doing a few hundred
    time.sleep(_sleep_period)
    if resp is not None and (resp.status_code == 200 or resp.status_code == 201):
        return resp.json()
    elif resp.status_code != 200 and resp.status_code != 201:
        print(resp.status_code)
        print(resp.text)
        raise requests.exceptions.RequestException
    else:
        return None


def put_src(url, body, api_key):
    err_lim = 5
    err_cnt = 1
    request_finished = False
    resp = None
    new_headers = _h
    new_headers['X-API-Key'] = api_key
    # print(f'attempting to request from:{url}')
    # usually fails if we are requesting too quickly, even with the sleep, try 10 times fail if still not working
    # after 10
    while not request_finished and err_cnt <= err_lim:
        # print(f'attempt: {err_cnt}')
        try:
            resp = requests.put(url, headers=new_headers, json=body)
            request_finished = True
            # print('request finished')
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print(f'Error Getting Response from {url}')
            print(e)
            if err_cnt == err_lim:
                raise requests.exceptions.RequestException
            err_cnt += 1
            print(f'sleeping for {_retry_sleep} before retry')
            time.sleep(_retry_sleep)
            print('retrying')
    # probably redundant, just being careful
    if err_cnt >= err_lim:
        print(f'err_cnt greater than err_limit {err_cnt} >= {err_lim}')
        raise requests.exceptions.RequestException
    # sleep so we don't get banned by requesting too much, .1,.2 give errors after doing a few hundred
    time.sleep(_sleep_period)
    if resp is not None and (resp.status_code == 200 or resp.status_code == 201):
        return resp.json()
    elif resp.status_code != 200 and resp.status_code != 201:
        print(resp.status_code)
        print(resp.text)
        raise requests.exceptions.RequestException
    else:
        return None
