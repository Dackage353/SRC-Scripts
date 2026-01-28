from common import fetch_handler, file_helper, reference, src_helper, tool, constants


FORCE_FETCH = False


if __name__ == '__main__':
    data = fetch_handler.get_series_info(constants.MAIN_SERIES, FORCE_FETCH)
    data.extend(fetch_handler.get_series_info(constants.SECONDARY_SERIES, FORCE_FETCH))

    games_without_levels = []

    for game_data in data:
        level_data = game_data.get('levels', {}).get('data')
        if len(level_data) == 0:
            name = game_data.get('names', {}).get('international')
            games_without_levels.append(name)

    print('\n'.join(games_without_levels))
    print(f'\n{len(games_without_levels)} games without levels out of {len(data)}')
