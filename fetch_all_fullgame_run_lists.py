from common import fetch_handler, file_helper, reference, src_helper, tool, constants


FORCE_FETCH = True


if __name__ == '__main__':
    categories = fetch_handler.get_all_fullgame_categories(constants.MAIN_SERIES, FORCE_FETCH)

    for category in categories:
        fetch_handler.fetch_category_run_list_data(category.id)
