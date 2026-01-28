from common import fetch_handler, file_helper, reference, src_helper, tool, constants


FORCE_FETCH = False


if __name__ == '__main__':
    fullgame_categories = fetch_handler.get_all_fullgame_categories(constants.MAIN_SERIES, FORCE_FETCH)
    fullgame_categories.extend(fetch_handler.get_all_fullgame_categories(constants.SECONDARY_SERIES, FORCE_FETCH))
    

    current_game_id = ''
    for category in fullgame_categories:
        if current_game_id != category.game_id:
            current_game_id = category.game_id
            
            if current_game_id != '':
                print('')
            
            game_name = fetch_handler.get_game_name(category.game_id)
            print(game_name)

        print(category.name)

    print(f'\nprinted {len(fullgame_categories)} categories')
