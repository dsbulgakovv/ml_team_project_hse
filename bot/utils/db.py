from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from constraints.sample_img import sample_img
from constraints.user_data import (
    ages_mapping,
    genders_mapping,
    incomes_mapping,
    kids_mapping,
)
from sqlalchemy import create_engine, text


engine_string = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def check_user(id):
    with create_engine(engine_string, echo=True).connect() as connection:
        results = connection.execute(
            text(f"SELECT * FROM users where user_id={id}")
        ).fetchall()
        if not results:
            add_user(id)
            return True
        return False


def add_user(id):
    with create_engine(engine_string, echo=True).connect() as connection:
        connection.execute(text(f"INSERT INTO users(user_id) VALUES ({id})"))
        connection.commit()


def set_age(id, age):
    if age in ages_mapping.keys():
        with create_engine(engine_string, echo=True).connect() as connection:
            connection.execute(
                text(f"UPDATE users SET age='{ages_mapping.get(age)}' where user_id={id}")
            )
            connection.commit()


def set_income(id, income):
    if income in incomes_mapping.keys():
        with create_engine(engine_string, echo=True).connect() as connection:
            connection.execute(
                text(
                    f"UPDATE users SET income='{incomes_mapping.get(income)}' where user_id={id}"
                )
            )
            connection.commit()


def set_sex(id, sex):
    if sex in genders_mapping.keys():
        with create_engine(engine_string, echo=True).connect() as connection:
            connection.execute(
                text(
                    f"UPDATE users SET sex={genders_mapping.get(sex)} where user_id={id}"
                )
            )
            connection.commit()


def set_kids(id, kids):
    if kids in kids_mapping.keys():
        with create_engine(engine_string, echo=True).connect() as connection:
            connection.execute(
                text(
                    f"UPDATE users SET kids_flg={kids_mapping.get(kids)} where user_id={id}"
                )
            )
            connection.commit()


def is_user_filled(id):
    with create_engine(engine_string, echo=True).connect() as connection:
        result = connection.execute(
            text(
                f"""SELECT * from users
         WHERE user_id={id} and ((age is not null) or (income is not null) or (sex is not null) or (kids_flg is not null))"""
            )
        ).fetchall()
        if result:
            return True
        return False


def get_movie_data(movie_id):
    with create_engine(engine_string, echo=True).connect() as connection:
        results = connection.execute(
            text(
                f"SELECT title, CAST(release_year as INTEGER), countries, genres, description FROM items where item_id={movie_id}"
            )
        ).fetchall()
        return results[0]


def get_movie_image(movie_id):
    with create_engine(engine_string, echo=True).connect() as connection:
        try:
            results = connection.execute(
                text(f"SELECT img_link FROM links WHERE item_id={movie_id}")
            ).fetchall()
            return results[0]
        except IndexError:
            return [sample_img]
