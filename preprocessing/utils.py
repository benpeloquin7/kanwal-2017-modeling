"""utils.py

Bespoke data preprocessing utils for Kanwall et al. (2017) data.

"""

import pandas as pd
import numpy as np


def process_line(l):
    return list(map(lambda x: x.strip(), l.split(', ')))


def file2df(f_path, condition):
    data = []
    with open(f_path, 'r') as f:
        header = process_line(f.readline())
        for l in f.readlines():
            if l == '\n':
                continue
            curr_line = process_line(l)
            data.append({hdr: d for hdr, d in zip(header, curr_line)})

    df = pd.DataFrame(data)
    df['condition'] = condition
    return df


def append_new_rows(x, missing_display_types, missing_label_types):
    n = len(missing_display_types)
    new_df = pd.DataFrame({
        'IP': np.repeat(set(x['IP']).pop(), n),
        'condition': np.repeat(set(x['condition']).pop(), n),
        'display_type': missing_display_types,
        'label_type': missing_label_types,
        'cnt': np.repeat(0, n)
    })
    x = x \
        .append(new_df) \
        .reset_index()
    return x


def fill_missing_rows(x):
    all_combns = set([
        ('frequent', 'long'),
        ('infrequent', 'short'),
        ('frequent', 'short'),
        ('infrequent', 'long')])

    available_items = set(list(zip(x['display_type'], x['label_type'])))
    missing_items = all_combns - available_items
    missing_display_types = [d for (d, l) in missing_items]
    missing_label_types = [l for (d, l) in missing_items]
    x = append_new_rows(x, missing_display_types, missing_label_types)
    return x


def add_n(x):
    """Add IP by condition by display type counts.

    That is, a person in the "combined" condition saw 24 instances of the
    common ('frequent') item and 8 instances of the infrequent item.

    """
    condition = x['condition'].values[0]
    if condition == 'combined':
        x['frequent_n'] = 24
        x['infrequent_n'] = 8
    elif condition == 'accuracy':
        x['frequent_n'] = 24
        x['infrequent_n'] = 8
    elif condition == 'time':
        x['frequent_n'] = 48
        x['infrequent_n'] = 16
    elif condition == 'neither':
        x['frequent_n'] = 48
        x['infrequent_n'] = 16
    else:
        raise Exception("{} condition unknown...".format())
    return x

def label_props(x):
    x['prop'] = x['cnt'] / sum(x['cnt'])
    return x


def save_df(df, fp):
    df.to_csv(fp)
