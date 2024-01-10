from utils.unpickle import CustomUnpickler


popularity_model = CustomUnpickler(
    open("artifacts/popular/popularity_based.pkl", "rb")
).load()


def get_movies():

    most_popular = popularity_model.predict()
    return most_popular
