# Используем базовый образ Python
FROM python:3.9

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="${PATH}:/root/.local/bin"

RUN poetry config virtualenvs.create false

WORKDIR /recsys

COPY pyproject.toml poetry.lock /recsys/
RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi --without bot,db,dev
RUN poetry run python -m pip install --no-use-pep517 --no-binary :all: lightfm


COPY ./.dvc /recsys/.dvc
COPY ./data.dvc ./artifacts.dvc /recsys/

COPY ./recsys /recsys/

RUN dvc pull

ENV PYTHONUNBUFFERED 1

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
