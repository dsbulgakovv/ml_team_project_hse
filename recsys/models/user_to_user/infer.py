from .utils import (
    data_find_best_content_u2u,
    get_pickle_artefact,
    get_prepaid_data,
    get_user_data_db,
    prepaid_user_data_u2u,
    show_10_recommendations_for_user,
)


knn = get_pickle_artefact("artifacts/user_to_user/model_user_to_user_39.pkl")
encoder = get_pickle_artefact("artifacts/user_to_user/encoder_user_to_user_39.pkl")
prepaid_data = get_prepaid_data(
    "artifacts/user_to_user/data_for_rec_model_user_to_user.csv"
)


def pipline_user_to_user(user_id: int, genre_input: str, content_type_input: str) -> list:
    """Func get user id, user choise, path to project (optional), return top 10 content

    1. Load data and artifacts
    2. SELECT to DB and get user infi
    2. Prepaid data for predict user cluster (with KNN model)
    3. Predict user cluster & Prepaid best films for user (Sort most popular selected content in user cluster)
    4. Prepaid top 10 films

    return: list with top 10 films for user
    """

    # 1. SELECT to DB and get user infi
    data_user = get_user_data_db(user_id)

    age = data_user[1]
    income = data_user[2]
    sex = data_user[3]
    kids_flg = int(data_user[4])

    # 2. prepaid user_data
    user_data = prepaid_user_data_u2u(encoder, age, income, sex, kids_flg)

    # 3. prepaid best film for user
    best_films_for_user = data_find_best_content_u2u(
        user_data, prepaid_data, knn, genre_input, content_type_input
    )

    # 4. prepaid top 10 films
    top_10_films = show_10_recommendations_for_user(best_films_for_user)

    return top_10_films
