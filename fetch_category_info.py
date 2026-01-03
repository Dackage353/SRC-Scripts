from common import fetch_handler, file_helper, reference, src_helper, tool


FORCE_FETCH = False

CATEGORY_IDS = [
    'rkl0e8kn'
]


if __name__ == '__main__':
    category_data = []

    for category_id in CATEGORY_IDS:
        data = fetch_handler.fetch_category_info(category_id, FORCE_FETCH)
        category_data.append(data)

    categories = tool.create_category_info_from_data(category_data)

    print(categories)
