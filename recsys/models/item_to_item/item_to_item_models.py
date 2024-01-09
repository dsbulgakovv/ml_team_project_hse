import pickle

from implicit.nearest_neighbours import BM25Recommender, TFIDFRecommender
from rectools.dataset import Dataset
from rectools.models import ImplicitItemKNNWrapperModel


class ItemToItemKnnTFIDF(ImplicitItemKNNWrapperModel):
    def __init__(self, k_nn: int = 10):
        self.k_nn = k_nn
        super().__init__(model=TFIDFRecommender(K=self.k_nn))

    def save_model(self, file_path: str = "my_model.pkl"):
        with open(file_path, "wb") as f:
            pickle.dump(self, f)

    def get_similar_items(self, target_item: int, dataset: Dataset, k: int = 10):
        rec_items_df = self.recommend_to_items(
            target_items=[target_item], dataset=dataset, k=k
        )
        rec_items_list = rec_items_df["item_id"].to_list()

        return rec_items_list


class ItemToItemKnnBM25(ImplicitItemKNNWrapperModel):
    def __init__(self, k_nn: int = 15, k1: float = 1.5, b: float = 0.9):
        self.k_nn = k_nn
        self.k1 = k1
        self.b = b
        super().__init__(model=BM25Recommender(K=self.k_nn, K1=self.k1, B=self.b))

    def save_model(self, file_path: str = "my_model.pkl"):
        with open(file_path, "wb") as f:
            pickle.dump(self, f)

    def get_similar_items(self, target_item: int, dataset: Dataset, k: int = 10):
        rec_items_df = self.recommend_to_items(
            target_items=[target_item], dataset=dataset, k=k
        )
        rec_items_list = rec_items_df["item_id"].to_list()

        return rec_items_list
