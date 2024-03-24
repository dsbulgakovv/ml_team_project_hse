import pickle

import pandas as pd
from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from sqlalchemy import create_engine, text


engine_string = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def get_pickle_artefact(file_path: str):
    """file_path это путь до артефакта в формате pickle, который возвращает сериализованную модель"""

    with open(file_path, "rb") as f:
        pickled_data = pickle.load(f)
        return pickled_data


def get_prepaid_data(file_path: str):
    """file_path это путь до предобработанного датасета в формате csv, который возвращает dataframe"""

    data_csv = pd.read_csv(file_path, sep=",")
    return data_csv


def prepaid_user_data_u2u(
    encoder, age: str, income: str, sex: str, kids_flg: int
) -> pd.DataFrame:
    """Функция преобразует стандартный набор данных о пользователе в данные для кластеризации KNN моделью"""

    encod_features = ["age", "income"]

    input_user_df = pd.DataFrame(
        {
            "user_id": [-1],
            "age": [age.replace("-", "_")],
            "income": [income.replace("-", "_")],
            "sex": [sex],
            "kids_flg": [int(kids_flg)],
        }
    )

    input_user_df["gender_man_flg"] = input_user_df["sex"].apply(
        lambda x: 1 if x == "М" else 0
    )

    input_user_df = input_user_df.drop("sex", axis=1)

    encoder_input_df = encoder.transform(input_user_df[encod_features])[0]  # ohe np array
    df_for_score_input = pd.DataFrame(columns=encoder.get_feature_names_out())
    df_for_score_input.loc[0] = encoder_input_df

    # Заменим категориальные фичи на новые бинаризованные.
    input_user_df = pd.concat(
        [input_user_df.drop(encod_features, axis=1), df_for_score_input], axis=1
    )

    return input_user_df


def data_find_best_content_u2u(
    data_to_score: pd.DataFrame,
    data_user_to_user_model: pd.DataFrame,
    model,
    genre,
    content_type,
) -> pd.Series:
    """Функция получает на вход информацию о клиенте, пожеланиях и на основе этого возвращает фильмы (рекомендации)"""

    data_to_score = data_to_score[model.feature_names_in_]  # Данные для кластеризации
    predict_cluster = model.predict(data_to_score)[0]  # Определяем кластер

    # Формируем DF с фильмами на основе пожеланий клиента. Ранжируем фильмы по "кол-ву просмотров"
    if (genre is None) & (content_type is None):  # Если жанр и тип контента пропуски
        pass
    elif (genre is None) & (
        content_type is not None
    ):  # Если жанр пропуск и тип контента заполнен
        best_films_for_user = data_user_to_user_model[
            (data_user_to_user_model["7_clusters"] == predict_cluster)
            & (data_user_to_user_model["content_type"] == f"{content_type}")
        ]["item_id"].value_counts()
    elif (genre is not None) & (
        content_type is None
    ):  # Если жанр заполнен и тип контента пропуск
        best_films_for_user = data_user_to_user_model[
            (data_user_to_user_model["7_clusters"] == predict_cluster)
            & (data_user_to_user_model[genre] == 1)
        ]["item_id"].value_counts()
    else:  # Если все заполнено
        best_films_for_user = data_user_to_user_model[
            (data_user_to_user_model["7_clusters"] == predict_cluster)
            & (data_user_to_user_model[genre] == 1)
            & (data_user_to_user_model["content_type"] == f"{content_type}")
        ]["item_id"].value_counts()

    return best_films_for_user


def show_10_recommendations_for_user(best_films_for_user: pd.Series):

    recommended_film = best_films_for_user[:10].index

    if len(recommended_film) > 0:

        return recommended_film.values

    return {"error": "no_films"}


def get_user_data_db(id):
    with create_engine(engine_string, echo=True).connect() as connection:
        result = connection.execute(
            text(
                f"""SELECT
                  user_id,
                  COALESCE(age, (SELECT MODE() WITHIN GROUP (ORDER BY age) FROM users)) AS age,
                  COALESCE(income, (SELECT MODE() WITHIN GROUP (ORDER BY income) FROM users)) AS income,
                  COALESCE(sex, (SELECT MODE() WITHIN GROUP (ORDER BY sex) FROM users)) AS sex,
                  COALESCE(kids_flg, (SELECT MODE() WITHIN GROUP (ORDER BY kids_flg) FROM users)) AS kids_flg
                FROM users
                WHERE user_id={id}"""
            )
        ).fetchall()

        return result[0]
