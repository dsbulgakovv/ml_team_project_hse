FROM python:3.9

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="${PATH}:/root/.local/bin"

WORKDIR /app

COPY ./db /app/

COPY ./get_data.sh /app/
RUN ./get_data.sh

COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-interaction --no-ansi


CMD ["poetry", "run", "python", "init-script.py"]