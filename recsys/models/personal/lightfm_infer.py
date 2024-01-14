import pickle

import numpy as np


dataset = pickle.load(open("artifacts/lightfm/lightfm_dataset.pkl", "rb"))
lightfm_model = pickle.load(open("artifacts/lightfm/lightfm_model.pkl", "rb"))


def is_user_present(user_id):
    return user_id in list(dataset._user_id_mapping.keys())


def get_movies(user_id):

    new_user_id = dataset._user_id_mapping[user_id]
    movies = list(dataset._item_id_mapping.values())
    preds = lightfm_model.predict([new_user_id] * len(movies), movies)
    sorted_preds = np.argsort(preds)[::-1][:10]
    reversed_mapping = {v: k for k, v in dataset._item_id_mapping.items()}
    movies = [reversed_mapping[x] for x in sorted_preds]
    return movies
