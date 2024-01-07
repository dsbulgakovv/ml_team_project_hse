# Используем базовый образ Python
FROM python:3.9

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="${PATH}:/root/.local/bin"

RUN poetry config virtualenvs.create false

WORKDIR /recsys

COPY pyproject.toml poetry.lock /recsys/
RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi --without bot,db,dev

COPY ./recsys /recsys/

COPY ./get_data.sh /recsys/
RUN ./get_data.sh

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED 1

# Запускаем приложение
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
