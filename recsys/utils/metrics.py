import numpy as np
import pandas as pd


def map_at_k(interactions: pd.DataFrame, predicts: pd.DataFrame, k: int):
    """Calculate MAP@K metric

    :param interactions: dataframe of users actual interactions
    :param predicts: dataframe of model's predictions
    :param k: amount of predictions to calculate metrics
    :return: Mean average precision at K
    """

    map_list = []
    for user in predicts["user_id"].values:
        user_interactions = interactions[interactions["user_id"] == user]
        user_predicts = predicts[predicts["user_id"] == user]
        max_k = min(len(user_interactions), k)
        user_precision = []
        for i in range(1, max_k + 1):
            precision = (
                len(
                    set(user_predicts["predict"].values[0][:i])
                    & set(user_interactions["item_id"].values[:i])
                )
                / i
            )
            user_precision.append(precision)
        map_list.append(np.mean(user_precision))
    return np.mean(map_list)
