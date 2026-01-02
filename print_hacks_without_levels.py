from common import fetch_handler


FORCE_FETCH = False


if __name__ == '__main__':
    data = fetch_handler.fetch_all_hack_info(FORCE_FETCH)

    hacks_without_levels = []

    for hack_data in data:
        level_data = hack_data.get('levels', {}).get('data')
        if len(level_data) == 0:
            name = hack_data.get('names', {}).get('international')
            hacks_without_levels.append(name)

    print('\n'.join(hacks_without_levels))
    print(f'\n{len(hacks_without_levels)} hacks without levels')
