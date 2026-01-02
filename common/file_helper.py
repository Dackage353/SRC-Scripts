from pathlib import Path
import json


CATEGORY_DIRECTORY = 'category_info_dump'
CATEGORY_RUN_LIST_DIRECTORY = 'category_run_list_dump'
LEADERBOARD_DIRECTORY = 'leaderboard_dump'
REFERENCE_DIRECTORY = 'reference'
HACK_INFO_DIRECTORY = 'hack_info'

ALL_HACK_INFO_FILE_NAME = 'all_hack_info.json'


def load_json(path):
    path = Path(str(path))

    with path.open('r') as file:
        return json.load(file)


def dump_json(data, path):
    path = Path(str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=4))


def make_text_file(text, file_name):
    path = Path(file_name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def make_csv_file_from_data_frame(df, path):
    path = Path(str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(str(path), index=False)
