import common.data_classes as data_classes
import common.file_handler as file_handler

# on srcom, click on the category name, the 'x=_____' in the url is the id
category_ids = [
    'rkl0e8kn',
    '9kvrj32g',
    'mkejomj2',
    'zd35lrkn'
]

if __name__ == '__main__':
    for category_id in category_ids:

        data = file_handler.fetch_category_run_list(category_id)
        runs = []

        for run_data in data:
            run = data_classes.Run.create_from_json(run_data)
            runs.append(run)

        df = file_handler.get_data_frame_for_run_list(runs)
        file_handler.make_csv_file_from_data_frame(df, f'output/run-list_{category_id}.csv')
