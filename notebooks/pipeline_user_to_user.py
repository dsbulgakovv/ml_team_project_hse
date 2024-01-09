import pickle

import pandas as pd
from artefacts_user_to_user import (
    create_user_df,
    data_find_best_content,
    show_10_recommendations_for_user,

)


# Загрузим df
data_user_to_user_model = pd.read_csv(
    "/Users/dan/git_repo/movs/project_1y/project_1223/ml_team_project_hse/artifacts/user_to_user/data_for_rec_model_user_to_user.csv",
    sep=",",
)

# Загрузим model
with open(
    "/Users/dan/git_repo/movs/project_1y/project_1223/ml_team_project_hse/artifacts/user_to_user/model_user_to_user_39.pkl",
    "rb",
) as f:
    model = pickle.load(f)

# Загрузим encoder
with open(
    "/Users/dan/git_repo/movs/project_1y/project_1223/ml_team_project_hse/artifacts/user_to_user/encoder_user_to_user_39.pkl",
    "rb",
) as f:
    encoder = pickle.load(f)


##############
# Ввоод данных от ползователя
age_input = input(
    "STR: 'age_25_34', 'age_18_24', 'age_45_54', 'age_35_44', 'age_55_64', 'age_65_inf': "
)
income_input = input(
    "STR: 'income_60_90', 'income_20_40', 'income_40_60', 'income_0_20', 'income_90_150', 'income_150_inf': "
)
sex_input = input("STR: 'М', 'Ж'")
kids_input = int(input("INT: 1 , 0 "))

# Создаем df для пользователя по введенным данным
input_user_df = create_user_df(
    encoder=encoder,
    age=age_input,
    income=income_input,
    sex=sex_input,
    kids_flg=kids_input,
)

##############
# Ввоод данных от ползователя
genre_type_input = input(
    """STR: 'hbo', 'боевики', 'вестерн', 'военные', 'детективы', 'детские', 'для взрослых', 'документальное', 'драмы',
    'иное', 'исторические', 'историческое', 'комедии', 'короткометражные', 'криминал', 'мелодрамы', 'мистика', 'музыка',
     'музыкальные', 'мультфильмы', 'полнометражные', 'приключения', 'развитие', 'развлекательные', 'семейное',
     'советские', 'спорт', 'триллеры', 'ужасы', 'фантастика': """
)

content_type_input = input("STR: 'series' 'film': ")

# Создаем df с рекомендациями для пользователя
best_films_for_user = data_find_best_content(
    data_to_score=input_user_df,
    data_user_to_user_model=data_user_to_user_model,
    model=model,
    genre=genre_type_input,
    content_type=content_type_input,
)

##############
<<<<<<< HEAD
show_10_recommendations_for_user(
    best_films_for_user=best_films_for_user, items_data=data_user_to_user_model
)
