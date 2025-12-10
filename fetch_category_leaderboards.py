import common.data_classes as data_classes
import common.file_handler as file_handler

# on srcom, click on the category name, the 'x=_____' in the url is the id
category_ids = [
    'rkl0e8kn',
    '9kvrj32g',
    'mkejomj2',
    'zd35lrkn',
]

if __name__ == '__main__':
    for category_id in category_ids:
        file_handler.fetch_leaderboard(category_id)
