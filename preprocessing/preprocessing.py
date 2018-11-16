"""preprocessing.py

Functionality for reading / pre-procesessing the Kanwall et al. 2017 data.

Raw data stored available here https://datashare.is.ed.ac.uk/handle/10283/2702.

If this file is run to .csv files will be output.

"""
import pandas as pd
from utils import *


def combine_raw_datasets():
    """Read in raw data from https://datashare.is.ed.ac.uk/handle/10283/2702.

    Combine condition types (combined, accuracy, time, neither)

    Minor preprocessing for label types.

    Returns
    -------
    pd.DataFrame
        DF of combined data.

    """
    dir_path = 'materials/kanwal-jasmeen-2017-data'
    f_combined_path = os.path.join(dir_path, "data_dyad_all_R_dem.csv")
    f_accuracy_path = os.path.join(dir_path, "data_partner_only_all_R_dem.csv")
    f_time_path = os.path.join(dir_path, "data_time_only_R_dem.csv")
    f_neither_path = os.path.join(dir_path, "data_min_R_dem.csv")

    df_combined = file2df(f_combined_path, 'combined')
    df_accuracy = file2df(f_accuracy_path, 'accuracy')
    df_time = file2df(f_time_path, 'time')
    df_neither = file2df(f_neither_path, 'neither')
    # Columns match
    assert all(df_combined.columns == df_accuracy.columns) and \
           all(df_time.columns == df_neither.columns)

    df_agg = df_combined.append(df_accuracy.append(df_time.append(df_neither)))
    df_agg['trial'] = df_agg['trial'].apply(lambda x: int(x))
    df_agg['display'] = df_agg['display'].apply(lambda x: int(x))

    # Update labels
    df_agg['label_type'] = df_agg['label'].apply(
        lambda x: 'short' if x == 'zop' else 'long')
    df_agg['display_type'] = df_agg['display'].apply(
        lambda x: 'frequent' if x < 2 else 'infrequent')

    return df_agg


def create_IP_probs_df(df_all_combined):
    # Props for use of 'short' form
    df_shorts = df_all_combined \
        .groupby(['IP', 'condition', 'display_type', 'label_type']) \
        .count()['L1'] \
        .reset_index() \
        .rename(columns={'L1': 'cnt'}) \
        .groupby(['IP', 'condition']) \
        .apply(fill_missing_rows) \
        .set_index(['IP']) \
        .reset_index() \
        .drop(columns=['index']) \
        .groupby(['IP', 'condition', 'display_type']) \
        .apply(label_props) \
        .drop(columns=['cnt']) \
        .query('label_type == "short"') \
        .pivot_table(values='prop', index=['IP', 'condition'],
                     columns=['display_type']) \
        .reset_index()
    df_shorts['label_type'] = 'short'
    df_shorts = pd.melt(df_shorts,
                        id_vars=['IP', 'condition', 'label_type'],
                        value_vars=['frequent', 'infrequent']) \
        .rename(columns={'value': 'prop_short'})

    # Props for use of 'long' form
    df_longs = df_all_combined \
        .groupby(['IP', 'condition', 'display_type', 'label_type']) \
        .count()['L1'] \
        .reset_index() \
        .rename(columns={'L1': 'cnt'}) \
        .groupby(['IP', 'condition']) \
        .apply(fill_missing_rows) \
        .set_index(['IP']) \
        .reset_index() \
        .drop(columns=['index']) \
        .groupby(['IP', 'condition', 'display_type']) \
        .apply(label_props) \
        .drop(columns=['cnt']) \
        .query('label_type == "long"') \
        .pivot_table(values='prop', index=['IP', 'condition'],
                     columns=['display_type']) \
        .reset_index()
    df_longs['label_type'] = 'long'
    df_longs = pd.melt(df_longs,
                       id_vars=['IP', 'condition', 'label_type'],
                       value_vars=['frequent', 'infrequent']) \
        .rename(columns={'value': 'prop_long'})

    merge_keys = ["IP", "condition", "display_type"]
    df_merged = pd.merge(df_longs, df_shorts, left_on=merge_keys,
                         right_on=merge_keys) \
        .drop(columns=["label_type_x", "label_type_y"])

    # Check that our proportions are proportions
    assert all(df_merged["prop_long"] + df_merged["prop_short"] == 1)
    return df_merged


if __name__ == '__main__':
    import argparse
    import logging
    import os

    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument('--out-dir', type=str,
                        default='data/',
                        help='Out directory [Default: "data/]')
    args = parser.parse_args()

# Save datas
if not os.path.exists(args.out_dir):
    os.makedirs(args.out_dir)

fp_raw_all = os.path.join(args.out_dir, 'preprocessed_all.csv')
fp_props_all = os.path.join(args.out_dir, 'props_all.csv')
df_raw_all = combine_raw_datasets()
df_all_proportions = create_IP_probs_df(df_raw_all)

logging.info("Caching {}".format(fp_raw_all))
df_raw_all.to_csv(fp_raw_all)
logging.info("Caching {}".format(fp_props_all))
df_all_proportions.to_csv(fp_props_all)
