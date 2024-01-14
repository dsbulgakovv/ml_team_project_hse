# Пайплайн обучения модели кластеризации пользователей
# А так же OHE кодировщика

import pickle
import warnings

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import OneHotEncoder
from tqdm import tqdm


warnings.filterwarnings("ignore")

# Загрузим данные
interactions = pd.read_csv(
    "/Users/dan/git_repo/movs/project_1y/project_1223/ml_team_project_hse/data/interactions.csv",
    sep=",",
)
items = pd.read_csv(
    "/Users/dan/git_repo/movs/project_1y/project_1223/ml_team_project_hse/data/items.csv",
    sep=",",
)
users = pd.read_csv(
    "/Users/dan/git_repo/movs/project_1y/project_1223/ml_team_project_hse/data/users.csv",
    sep=",",
)

# Заполним пропуски модой пропуски
inc_moda = users["income"].mode()
for row in tqdm(range(len(users))):
    if type(users["income"].loc[row]) != str:
        users["income"].loc[row] = inc_moda[0]

age_moda = users["age"].mode()
for row in tqdm(range(len(users))):
    if type(users["age"].loc[row]) != str:
        users["age"].loc[row] = age_moda[0]

age_moda = users["age"].mode()
for row in tqdm(range(len(users))):
    if type(users["age"].loc[row]) != str:
        users["age"].loc[row] = age_moda[0]

# Категориальны переменные

# Категориальные переменные в бинарные

users["gender_man_flg"] = users["sex"].apply(lambda x: 1 if x == "М" else 0)
users = users.drop("sex", axis=1)

# Фичи, которые будем преобразовывать
encod_features = ["age", "income"]

# Получим новый df с преобразованными фичами
encoder = OneHotEncoder(sparse=False)
df_encoded_features = pd.DataFrame(encoder.fit_transform(users[encod_features]))
df_encoded_features.columns = encoder.get_feature_names_out()

df_encoded_features.head()

# Заменим категориальные фичи на новые бинаризованные.
users = pd.concat([users.drop(encod_features, axis=1), df_encoded_features], axis=1)

users.head()

# models

knn = KMeans(n_clusters=7)
knn.fit(users)

# save artefats

# save model
with open("model_user_to_user_39.pkl", "wb") as f:
    # Сохраняем объект в файл
    pickle.dump(knn, f)

# save encoder
with open("encoder_user_to_user_39.pkl", "wb") as f:
    # Сохраняем объект в файл
    pickle.dump(encoder, f)

print("done")
