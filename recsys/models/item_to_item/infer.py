import pickle
import warnings

from item_to_item_models import ItemToItemKnnBM25, ItemToItemKnnTFIDF
from rectools.dataset import Dataset


def data_pkl_loader(file_path: str):
    with open(file_path, "rb") as f:
        data = pickle.load(f)
        return data


def infer_item_to_item_model_loader(file_path: str):
    with open(file_path, "rb") as f:
        model = pickle.load(f)
    try:
        assert model.__class__ in [ItemToItemKnnBM25, ItemToItemKnnTFIDF]
    except AssertionError:
        warnings.warn(
            "The model you are trying to import is not ItemToItemKnnBM25, ItemToItemKnnTFIDF.",
            RuntimeWarning,
            stacklevel=2,
        )

    return model


def get_similar_items_inference(
    model_file_path: str, target_item: int, dataset: Dataset, k: int
):
    model = infer_item_to_item_model_loader(model_file_path)
    similar_items = model.get_similar_items(target_item=target_item, dataset=dataset, k=k)

    return similar_items


def _main():
    outer_path = "../../../"
    artifacts_path = outer_path + "artifacts/item_to_item/"
    model_path = artifacts_path + "knn_bm25_model.pkl"
    dataset_path = artifacts_path + "train_dataset.pkl"
    sample_target = 9506
    dataset = data_pkl_loader(dataset_path)
    k_recommended = 10
    recommended_items = get_similar_items_inference(
        model_file_path=model_path,
        target_item=sample_target,
        dataset=dataset,
        k=k_recommended,
    )
    print(recommended_items)


if __name__ == "__main__":
    _main()
