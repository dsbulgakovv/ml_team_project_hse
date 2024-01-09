from typing import List, Union

import numpy as np
import pandas as pd
from infer import data_pkl_loader, item_to_item_model_loader
from item_to_item_models import ItemToItemKnnBM25, ItemToItemKnnTFIDF
from rectools.dataset import Dataset
from rectools.metrics import MAP, MeanInvUserFreq, Serendipity, calc_metrics


def agg_metrics(k_list: List[int]):
    metrics = {}
    for k_val in k_list:
        metrics[f"MAP@{k_val}"] = MAP(k=k_val)
        metrics[f"Novelty@{k_val}"] = MeanInvUserFreq(k=k_val)
        metrics[f"Serendipity@{k_val}"] = Serendipity(k=k_val)

    return metrics


def infer_and_calc_metrics_on_users(
    model: Union[ItemToItemKnnBM25, ItemToItemKnnTFIDF],
    dataset_item_features: Dataset,
    test_users: np.ndarray,
    test: pd.DataFrame,
    train: pd.DataFrame,
    catalog: np.ndarray,
    k_list: List[int],
) -> dict:

    metrics = agg_metrics(k_list=k_list)
    test_users_recommends = model.recommend(
        users=test_users,
        dataset=dataset_item_features,
        k=10,
        filter_viewed=True,
    )

    metric_values = calc_metrics(metrics, test_users_recommends, test, train, catalog)

    return metric_values


def _main() -> None:
    outer_path = "../../../"
    artifacts_path = outer_path + "artifacts/item_to_item/"
    model_path = artifacts_path + "knn_bm25_model.pkl"
    dataset_path = artifacts_path + "train_dataset.pkl"
    test_users_path = artifacts_path + "test_users_sample.pkl"
    test_path = artifacts_path + "test.pkl"
    train_path = artifacts_path + "train.pkl"
    catalog_path = artifacts_path + "items_catalog.pkl"

    model = item_to_item_model_loader(model_path)
    dataset = data_pkl_loader(dataset_path)
    test_users = data_pkl_loader(test_users_path)
    test = data_pkl_loader(test_path)
    train = data_pkl_loader(train_path)
    catalog = data_pkl_loader(catalog_path)

    metric_values = infer_and_calc_metrics_on_users(
        model=model,
        dataset_item_features=dataset,
        test_users=test_users,
        test=test,
        train=train,
        catalog=catalog,
        k_list=[1, 10],
    )

    print(metric_values)


if __name__ == "__main__":
    _main()
