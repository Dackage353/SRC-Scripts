from common import fetch_handler, file_helper, reference, src_helper, tool, constants


FORCE_FETCH = False
USER_ID = 'qxkrpqm8'


if __name__ == '__main__':
    fullgame_categories = fetch_handler.get_all_fullgame_categories(constants.MAIN_SERIES, FORCE_FETCH)
    fullgame_categories.extend(fetch_handler.get_all_fullgame_categories(constants.SECONDARY_SERIES, FORCE_FETCH))
    fullgame_categories_dict = {c.id: c for c in fullgame_categories}

    run_list = fetch_handler.get_user_run_list(USER_ID, FORCE_FETCH)

    categories_filled = set()
    fill_count = 0

    for run in run_list:
        if run.category_id in fullgame_categories_dict and run.category_id not in categories_filled:
            categories_filled.add(run.category_id)

            category = fullgame_categories_dict[run.category_id]
            print(f'{category.game_and_category_name}')

    print(f'\ntotal fillrate: {len(categories_filled)} / {len(fullgame_categories)}')
