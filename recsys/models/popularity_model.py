import pandas as pd


class PopularityModel:
    def __init__(self, n: int):
        self.n = n
        self.top_n = []

    def fit(self, df: pd.DataFrame):
        self.top_n = df.loc[:, "item_id"].value_counts()[: self.n].index.tolist()

    def predict(self):
        predicts = self.top_n
        return predicts
