import pickle


class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if name == "PopularityModel":
            from models.personal.popularity_model import PopularityModel

            return PopularityModel
        return super().find_class(module, name)
