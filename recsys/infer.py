import pickle
import sys
import pandas as pd

from recsys import models

sys.modules['models'] = models
items = pd.read_csv('data/items.csv')
popularity_model = pickle.load(open('recsys/trained_models/popularity_based.pkl', 'rb'))


def get_movie():

    preds = popularity_model.predict()
    for pred in preds:
        item = items[items['item_id'] == pred]
        yield item.to_dict('records')[0]
