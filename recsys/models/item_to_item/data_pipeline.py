import pickle
from typing import List

import numpy as np
import pandas as pd
from rectools import Columns
from rectools.dataset import Dataset


def make_flatten_feature_df(
    train: pd.DataFrame, item_features: pd.DataFrame, split_by_coma_cols: List[str]
):
    items = item_features.loc[
        item_features[Columns.Item].isin(train[Columns.Item])
    ].copy()
    for col in split_by_coma_cols:
        items[col] = (
            items[col].str.lower().str.replace(", ", ",", regex=False).str.split(",")
        )

    dfs_features_list = list()
    for col in split_by_coma_cols:
        temp_df = items[["item_id", col]].explode(col)
        temp_df.columns = ["id", "value"]
        temp_df["feature"] = col
        dfs_features_list.append(temp_df)

    rest_features = list(
        set(items.drop("item_id", axis=1).columns) - set(split_by_coma_cols)
    )
    for col in rest_features:
        temp_df = items.reindex(columns=[Columns.Item, col])
        temp_df.columns = ["id", col]
        temp_df["feature"] = col
        dfs_features_list.append(temp_df)

    items_flatten = pd.concat(dfs_features_list)

    return items_flatten


def prepare_data(
    items_data_path: str, cat_item_features: List[str], interactions_data_path: str
):
    items_df = pd.read_csv(items_data_path)
    interactions = pd.read_csv(
        interactions_data_path, parse_dates=["last_watch_dt"]
    ).rename(columns={"last_watch_dt": Columns.Datetime})
    items_features = items_df[
        [
            "item_id",
            "release_year",
            "for_kids",
            "age_rating",
            "genres",
            "countries",
            "keywords",
            "title",
            "description",
        ]
    ]
    values = {
        "for_kids": 0,
        "age_rating": items_features.median(numeric_only=True).age_rating,
        "release_year": items_features.median(numeric_only=True).release_year,
        "countries": "unknown",
        "keywords": "unknown",
        "description": "unknown",
    }
    items_features = items_features.fillna(value=values)

    # Process interactions
    interactions[Columns.Weight] = np.where(interactions["watched_pct"] > 10, 3, 1)

    # Split to train / test
    max_date = interactions[Columns.Datetime].max()
    train = interactions[
        interactions[Columns.Datetime] < max_date - pd.Timedelta(days=7)
    ].copy()
    test = interactions[
        interactions[Columns.Datetime] >= max_date - pd.Timedelta(days=7)
    ].copy()
    train.drop(train.query("total_dur < 300").index, inplace=True)
    cold_users = set(test[Columns.User]) - set(train[Columns.User])
    test.drop(test[test[Columns.User].isin(cold_users)].index, inplace=True)
    test_users = test[Columns.User].unique()
    catalog = train[Columns.Item].unique()

    # Process item features to the form of a flatten dataframe
    item_features = make_flatten_feature_df(
        train=train, item_features=items_features, split_by_coma_cols=cat_item_features
    )

    # Make rectools.Dataset from pandas.DataFrame
    dataset_item_features = Dataset.construct(
        interactions_df=train,
        item_features_df=item_features,
        cat_item_features=cat_item_features,
    )

    return dataset_item_features, test_users, catalog, train, test


def _main():
    categorical_item_features = ["genres", "countries", "keywords"]
    outer_path = "../../../"
    data_path = outer_path + "data/"
    artifacts_path = outer_path + "artifacts/item_to_item/"

    dataset, test_users_sample, items_catalog, train, test = prepare_data(
        items_data_path=data_path + "items.csv",
        cat_item_features=categorical_item_features,
        interactions_data_path=data_path + "interactions.csv",
    )
    artifacts_dict = dict()
    artifacts_dict["train_dataset.pkl"] = dataset
    artifacts_dict["test_users_sample.pkl"] = test_users_sample
    artifacts_dict["items_catalog.pkl"] = items_catalog
    artifacts_dict["train.pkl"] = train
    artifacts_dict["test.pkl"] = test

    for file_name, data_object in artifacts_dict.items():
        with open(artifacts_path + file_name, "wb") as f:
            pickle.dump(data_object, f)


if __name__ == "__main__":
    _main()
