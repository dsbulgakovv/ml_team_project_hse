from sqlalchemy import create_engine, text

dbname = "test"
user = "admin"
password = "admin"
host = "postgres"
port = "5432" # TODO в конфиг
engine_string = f'postgresql://{user}:{password}@{host}:{port}/{dbname}'


def check_user(id):
    with create_engine(engine_string, echo=True).connect() as connection:
        results = connection.execute(text(f'SELECT * FROM users where user_id={id}')).fetchall()
        if not results:
            add_user(id)
            return True
        return False


def add_user(id):
    with create_engine(engine_string, echo=True).connect() as connection:
        connection.execute(text(f"INSERT INTO users(user_id) VALUES ({id})"))
        connection.commit()


def set_age(id, age):
    ages = {
        '18-24': 'age_18_24',
        '25-34': 'age_25-34',
        '35-44': 'age_35-44',
        '45-54': 'age_18_24',
        '55-64': 'age_45-54',
        '65+': 'age_65_inf',
    }
    if age in ages.keys():
        with create_engine(engine_string, echo=True).connect() as connection:
            connection.execute(text(f"UPDATE users SET age='{ages.get(age)}' where user_id={id}"))
            connection.commit()


def set_income(id, income):
    incomes = {
        '0-20к': 'income_0_20',
        '20-40к': 'income_20_40',
        '40-60к': 'income_40_60',
        '60-90к': 'income_60_90',
        '90-150к': 'income_90_150',
        '150к+': 'income_150_inf'
    }
    if income in incomes.keys():
        with create_engine(engine_string, echo=True).connect() as connection:
            connection.execute(text(f"UPDATE users SET income='{incomes.get(income)}' where user_id={id}"))
            connection.commit()


def set_sex(id, sex):
    sexes = {
        'м': 0,
        'ж': 1,
    }
    if sex in sexes.keys():
        with create_engine(engine_string, echo=True).connect() as connection:
            connection.execute(text(f"UPDATE users SET sex={sexes.get(sex)} where user_id={id}"))
            connection.commit()


def set_kids(id, kids):
    kid_mapping = {
        'да': 1,
        'нет': 0
    }
    if kids in kid_mapping.keys():
        with create_engine(engine_string, echo=True).connect() as connection:
            connection.execute(text(f"UPDATE users SET kids_flg={kid_mapping.get(kids)} where user_id={id}"))
            connection.commit()


def is_user_filled(id):
    with create_engine(engine_string, echo=True).connect() as connection:
        result = connection.execute(text(f"""SELECT * from users
         WHERE user_id={id} and ((age is not null) or (income is not null) or (sex is not null) or (kids_flg is not null))""")).fetchall()
        if result:
            return True
        return False
