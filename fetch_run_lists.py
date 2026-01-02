from common import fetch_handler


FORCE_FETCH = False

# on srcom, click on the category name, the 'x=_____' in the url is the id
CATEGORY_IDS = [
    'rkl0e8kn',
    '9kvrj32g',
    'mkejomj2',
    'zd35lrkn'
]


if __name__ == '__main__':
    fetch_handler.fetch_category_run_lists(CATEGORY_IDS, FORCE_FETCH)
