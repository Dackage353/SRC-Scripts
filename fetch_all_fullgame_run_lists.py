from common import data_handler, fetch_handler, file_helper, reference


FORCE_FETCH = False


if __name__ == '__main__':
    categories = fetch_handler.fetch_all_fullgame_categories(FORCE_FETCH)

    for category in categories:
        fetch_handler.fetch_category_run_list_data(category.id, FORCE_FETCH)
