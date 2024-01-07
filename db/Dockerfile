FROM python:3.9

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="${PATH}:/root/.local/bin"

WORKDIR /app

COPY ./db /app/

COPY pyproject.toml poetry.lock /app/
RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi --no-root --without bot,recsys,dev

COPY ./.dvc /app/.dvc
COPY ./data.dvc ./trained_models.dvc /app/
RUN dvc pull data


CMD ["poetry", "run", "python", "init-script.py"]
