FROM python:3.9

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="${PATH}:/root/.local/bin"

RUN poetry config virtualenvs.create false

WORKDIR /app

COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-interaction --no-ansi


COPY ./bot /app/

CMD ["python", "app.py"]
