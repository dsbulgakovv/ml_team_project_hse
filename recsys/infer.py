import pickle
import sys

import models
import pandas as pd


sys.modules["models"] = models
items = pd.read_csv("data/items.csv")
popularity_model = pickle.load(open("artifacts/popular/popularity_based.pkl", "rb"))


def get_movies():

    most_popular = popularity_model.predict()
    return most_popular
