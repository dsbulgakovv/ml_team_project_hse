import os
import pickle
from pathlib import Path

import pandas as pd
from models.popularity_model import PopularityModel
from utils.helpers import split_df
from utils.metrics import map_at_k


def train_model(interactions_df: pd.DataFrame, n_days):
    train, test = split_df(interactions_df, n_days)
    model = PopularityModel(n=10)
    model.fit(train)
    test_users = pd.DataFrame({"user_id": test["user_id"].unique()})
    test_users["predict"] = test_users.apply(lambda x: model.predict(), axis=1)
    map_at_10 = map_at_k(test, test_users, 10)
    print(f"MAP@10: {map_at_10}")
    return model


if __name__ == "__main__":
    interactions = pd.read_csv("data/interactions.csv")
    model = train_model(interactions, 7)
    path_to_save_model = Path("recsys/trained_models")
    if not os.path.isdir(path_to_save_model):
        os.mkdir(path_to_save_model)
    pickle.dump(model, open(path_to_save_model / "popularity_based.pkl", "wb"))
