# import pickle
import pandas as pd


encod_features = ["age", "income"]


def create_user_df(
    encoder, age: str, income: str, sex: str, kids_flg: int
) -> pd.DataFrame:
    """Функция принимает на вход данные от пользователя (черех ТГ бота)

    Пользователь вводит информацию о себе используя кнопки в телеграмме (фиксированные ответы):
    age: 'age_18_24', 'age_25_34', 'age_45_54', 'age_35_44', 'age_55_64', 'age_65_inf'
    income: 'income_0_20', 'income_20_40', 'income_40_60', 'income_60_90', 'income_90_150', 'income_150_inf'
    sex: 'М', 'Ж'
    kids_flg: 1, 0

    Далее происходит
        * Формирование DF
        * Преобразование бинарного столбца sex
        * OHE кодирование

    На выходе получаемм готовый DF для кластеризации
    """

    # Формирование DF
    input_user_df = pd.DataFrame(
        {
            "user_id": [-1],
            "age": [age],
            "income": [income],
            "sex": [sex],
            "kids_flg": [kids_flg],
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


def data_find_best_content(
    data_to_score: pd.DataFrame,
    data_user_to_user_model: pd.DataFrame,
    model,
    genre: str,
    content_type: str,
) -> pd.Series:
    """Функция получает на вход информацию о клиенте, пожеланиях и на основе этого возвращает фильмы (рекомендации)

    Пользователь вводит информацию о пожеланиях используя кнопки в телеграмме (фиксированные ответы), а так же ранее агрегированные данные:
    genre: 'ужасы', 'боевики' и тд
    content_type: 'series' 'film'

    data_to_score - это данные полученные из функции create_score_df
    data_user_to_user_model - это датасет с информацией о кластере клиента и фильмах которые он смотрел. На основе него агрегируем
    информацию о популярности фильмов
    model - моделькластеризации

    Далее происходит
        * Выбираем кластер для клиента
        * Формируем DF с фильмами на основе пожеланий клиента. Ранжируем фильмы по "кол-ву просмотров"
        * OHE кодирование

    На выходе pd.Series, где индексы - это item_id, расположенные по популярности у пользователей из этого же кластера
    по этим же предпосчтениям (если они указаны)
    """
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


def show_recommendations(best_films_for_user: pd.Series, items_data: pd.DataFrame):
    input_val = "next"
    start = 0  # Стартовый номер рекмендации на 1 иетрации (индекс)
    stop = 10  # Последний номер рекмендации на 1 иетрации (индекс)
    i = 1  # Порядковый номер рекомендации

    while input_val == "next":

        recomendet_film = best_films_for_user[start:stop].index

        if start == 0:
            print("Составляем рекомендации на основе похожих на вас пользователей...")

        # Навесим на id рекомендуемых фильмов инфу из items
        df_to_show_index = pd.DataFrame(recomendet_film, columns=["item_id"])
        df_to_show = items_data.merge(
            df_to_show_index, how="inner", on="item_id"
        )  # тут ходим в табличку items за описанием по 10 фильмам

        # Выводим контент
        if len(best_films_for_user) > start:  # Пока есть контент - выведем его
            print("Рекомендуем посмотреть следущие фильмы: ")

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
                print(
                    f"{i}. {content}: {title_show}, год выпуска: {year_show}, жанр: {genres_show}"
                )
                i = i + 1
        else:
            print(
                "Больше подходящего контента у нас нет :( попробуйте изменить критерии поиск"
            )

        # Обновим индексы для следующего отображения
        start = start + 10
        stop = stop + 10

        # Продолжаем или останавливаемя ('next'?) - кнопка из ТГ
        input_val = input("next для следующих рекомендаций: ")
