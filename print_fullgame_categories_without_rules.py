from common import data_handler, fetch_handler, file_helper, reference


FORCE_FETCH = False


if __name__ == '__main__':
    categories = fetch_handler.fetch_all_fullgame_categories(FORCE_FETCH)

    current_game_id = ''
    count = 0
    for category in categories:
        if category.rules is None:
            count += 1

            if current_game_id != category.game_id:
                current_game_id = category.game_id
                
                if current_game_id != '':
                    print('')
                
                game_name = fetch_handler.fetch_game_name(category.game_id)
                print(game_name)

            print(category.name)

    print(f'\n{count} out of {len(categories)} fullgame categories don\'t have rules')
