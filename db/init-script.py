from time import sleep

import pandas as pd
from sqlalchemy import create_engine


sleep(10)

dbname = "test"
user = "admin"
password = "admin"
host = "postgres"
port = "5432"  # TODO в конфиг
engine = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

df_users = pd.read_csv("data/users.csv")
engine_users = create_engine(engine)
df_users.to_sql("users", engine_users, index=False, if_exists="replace")

df_items = pd.read_csv("data/items.csv")
engine_items = create_engine(engine)
df_items.to_sql("items", engine_items, index=False, if_exists="replace")

df_interactions = pd.read_csv("data/interactions.csv")
engine_interactions = create_engine(engine)
df_interactions.to_sql(
    "interactions", engine_interactions, index=False, if_exists="replace"
)
