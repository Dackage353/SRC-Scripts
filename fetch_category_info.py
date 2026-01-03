from common import data_handler, fetch_handler, file_helper, reference


FORCE_FETCH = False

CATEGORY_IDS = [
    'rkl0e8kn'
]


if __name__ == '__main__':
    category_data = []

    for category_id in CATEGORY_IDS:
        data = fetch_handler.fetch_category_info(category_id, FORCE_FETCH)
        category_data.append(data)

    categories = data_handler.create_category_info_from_data(category_data)

    print(categories)
