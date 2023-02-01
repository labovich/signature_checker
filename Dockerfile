FROM python:3.10-slim

WORKDIR /app

ADD pyproject.toml poetry.lock ./
RUN pip install -U pip && pip install wheel poetry
RUN poetry config virtualenvs.create false && poetry install

ADD . .

ENTRYPOINT [ "poetry", "run", "flask", "--app", "app", "run", "--host", "0.0.0.0"]