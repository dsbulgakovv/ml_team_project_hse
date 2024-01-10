from models.personal.lightfm_infer import get_movies as lightfm_movies
from models.personal.lightfm_infer import is_user_present
from models.personal.popularity_infer import get_movies as popular_movies


def get_movies_for_user(user_id):
    present = is_user_present(user_id)
    if present:
        return lightfm_movies(user_id)
    else:
        return popular_movies()
