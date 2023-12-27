# Используем базовый образ Python
FROM python:3.9

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="${PATH}:/root/.local/bin"

RUN poetry config virtualenvs.create false

# Создаем директорию приложения внутри контейнера
WORKDIR /recsys

COPY pyproject.toml poetry.lock /recsys/
RUN poetry install --no-interaction --no-ansi

COPY ./recsys /recsys/
COPY ./proto /recsys/proto
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. proto/service.proto

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED 1

# Запускаем приложение
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
