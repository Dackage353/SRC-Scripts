from common import fetch_handler, file_helper, reference, src_helper, tool


FORCE_FETCH = False


if __name__ == '__main__':
    data = fetch_handler.fetch_series_info(FORCE_FETCH)

    hacks_with_1 = []
    hacks_with_2 = []
    hacks_with_3 = []
    other_hacks = []

    for hack_data in data:
        platforms = hack_data.get('platforms')

        name = hack_data.get('names', {}).get('international')
        if len(platforms) == 1:
            hacks_with_1.append(name)
        elif len(platforms) == 2:
            hacks_with_2.append(name)
        elif len(platforms) == 3:
            hacks_with_3.append(name)

    print('hacks with 1 platform\n-----')
    print('\n'.join(hacks_with_1))

    print('\nhacks with 2 platforms\n-----')
    print('\n'.join(hacks_with_2))

    print('\nhacks with 3 platforms\n-----')
    print('\n'.join(hacks_with_3))

    #print('\nhacks without 1-3 platforms\n-----')
    #print('\n'.join(other_hacks))

    print(f'\n{len(hacks_with_1)} have 1 platform')
    print(f'{len(hacks_with_2)} have 2 platforms')
    print(f'{len(hacks_with_3)} have 3 platforms')
    #print(f'{len(other_hacks)} without 1-3 platforms')
    