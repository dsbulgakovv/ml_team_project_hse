import pickle

import pandas as pd


def get_pickle_artefact(file_path: str):
    """file_path это путь до артефакта в формате pickle, который возвращает сериализованную модель"""
    with open(
        file_path,
        "rb",
    ) as f:
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

    # Для OHE кодирования
    encod_features = ["age", "income"]

    # Формирование DF
    input_user_df = pd.DataFrame(
        {
            "user_id": [-1],
            "age": [
                age[0]
            ],  # Костыль - передаю в функцию строчку, а преобразуется в кортеж
            "income": [
                income[0]
            ],  # Костыль - передаю в функцию строчку, а преобразуется в кортеж
            "sex": [
                sex[0]
            ],  # Костыль - передаю в функцию строчку, а преобразуется в кортеж
            "kids_flg": [
                int(kids_flg[0])
            ],  # Костыль - передаю в функцию строчку, а преобразуется в кортеж
        }
    )

    # Преобразование бинарного столбца sex
    input_user_df["gender_man_flg"] = input_user_df["sex"].apply(
        lambda x: 1 if x == "М" else 0
    )

    input_user_df = input_user_df.drop("sex", axis=1)

    # OHE кодирование
    encoder_input_df = encoder.transform(input_user_df[encod_features])[0]  # ohe np array
    df_for_score_input = pd.DataFrame(
        columns=encoder.get_feature_names_out()
    )  # ohe df (only columns)
    df_for_score_input.loc[0] = encoder_input_df  # ohe df add data

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

    genre = genre[0]  # Костыль - передаю в функцию строчку, а преобразуется в кортеж
    # content_type = content_type[0]

    # Выбираем кластер для клиента

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


def show_10_recommendations_for_user(
    best_films_for_user: pd.Series, items_data: pd.DataFrame
):

    i = 1  # Порядковый номер рекомендации
    top_10_films = dict()  # Сложим топ 10 фильмов сюда

    recomendet_film = best_films_for_user[:10].index

    if len(recomendet_film) > 0:  # Если есть контент - выведем его
        # print("Составляем рекомендации на основе похожих на вас пользователей...")

        # Навесим на id рекомендуемых фильмов инфу из items
        df_to_show_index = pd.DataFrame(recomendet_film, columns=["item_id"])
        df_to_show = items_data.merge(
            df_to_show_index, how="inner", on="item_id"
        )  # тут ходим в табличку items за описанием по 10 фильмам

        # Выводим контент

        # print("Рекомендуем посмотреть следущие фильмы: ")

        for film in recomendet_film:  # Итерируемся по каждому фильму
            # Собираем инфу о фильме в переменные
            rec = df_to_show[df_to_show["item_id"] == film][
                ["title", "release_year", "genres", "content_type"]
            ]

            if rec["content_type"].iloc[0] == "film":
                content = "Фильм"
            else:
                content = "Сериал"

            year_show = int(rec["release_year"].iloc[0])
            title_show = rec["title"].iloc[0]
            genres_show = rec["genres"].iloc[0]

            # Выводим контент
            content = f"{i}. {content}: {title_show}, год выпуска: {year_show}, жанр: {genres_show}"

            top_10_films[i] = content

            i = i + 1

        return top_10_films

    else:
        top_10_films["error"] = "no_films"
        return top_10_films
        # print("Подходящего контента у нас нет :( попробуйте изменить критерии поиска")
