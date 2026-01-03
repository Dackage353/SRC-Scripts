from pathlib import Path
import json

import pandas as pd

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


def make_csv_file_from_data_frame(df, path, index=False):
    path = Path(str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(str(path), index=index)


def make_single_sort_csv(df, path, sort_id, sort_name, ref, add_empties=False):
    counts = (
        df
        .groupby([sort_id])
        .size()
    )

    if add_empties:
        counts = counts.reindex(ref.keys(), fill_value=0)

    out = (
        counts
        .rename('count')
        .reset_index()
    )

    out[sort_name] = out[sort_id].map(ref)

    out = (
        out
        [[sort_name, 'count']]
        .sort_values(by=['count', sort_name], ascending=[False, True])
    )

    out.to_csv(path, index=False)

def make_double_sort_csv(df, path, sort1_id, sort2_id, sort1_name, sort2_name, ref1, ref2, all_pairs):
    counts = df.groupby([sort1_id, sort2_id]).size()

    full_index = pd.MultiIndex.from_tuples(all_pairs, names=[sort1_id, sort2_id])
    counts = counts.reindex(full_index, fill_value=0)

    out = counts.reset_index(name='count')


    out[sort1_name] = out[sort1_id].map(ref1)
    out[sort2_name] = out[sort2_id].map(ref2)

    out = (
        out
        [[sort1_name, sort2_name, 'count']]
        .sort_values(by=['count', sort1_name, sort2_name], ascending=[False, True, True])
    )

    out.to_csv(path, index=False)