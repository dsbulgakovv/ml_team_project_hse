from typing import Union

from infer import data_pkl_loader
from item_to_item_models import ItemToItemKnnBM25, ItemToItemKnnTFIDF
from rectools.dataset import Dataset


def training_model(model: Union[ItemToItemKnnBM25, ItemToItemKnnTFIDF], dataset: Dataset):
    model_for_export = model
    model_for_export.fit(dataset)

    return model_for_export


def _main():
    outer_path = "../../../"
    artifacts_path = outer_path + "artifacts/item_to_item/"
    model_path = artifacts_path + "knn_bm25_model.pkl"
    dataset_path = artifacts_path + "train_dataset.pkl"
    dataset = data_pkl_loader(dataset_path)
    base_model = ItemToItemKnnBM25()
    trained_model = training_model(base_model, dataset)
    trained_model.save_model(model_path)


if __name__ == "__main__":
    _main()
