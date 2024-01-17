FROM python:3.10.13

WORKDIR /usr/src/app/itmo_case6

COPY poetry.lock pyproject.toml /usr/src/app/itmo_case6/

RUN pip install poetry

RUN poetry install --no-dev

COPY . /usr/src/app/itmo_case6/

CMD ["poetry", "run","python", "-m", "src.backend.app"]
