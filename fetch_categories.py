import src_helper
import json
import file_handler
from pathlib import Path

# on srcom, click on the category name, the 'x=_____' in the url is the id
category_ids = [
    'rkl0e8kn',
    '9kvrj32g',
    'mkejomj2',
    'zd35lrkn',
]

if __name__ == '__main__':
    for category_id in category_ids:
        data = file_handler.fetch_leaderboard_data(category_id)
