FROM python:3.9.5

ARG ENV

ENV ENV=$ENV} \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # pip:
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry:
    POETRY_VERSION=1.1.7 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    PATH="$PATH:/root/.poetry/bin"

RUN apt-get update && apt-get upgrade -y \
  && apt-get install --no-install-recommends -y curl \
  && curl -sSL 'https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py' | python \
  && poetry --version \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY ./poetry.lock ./pyproject.toml ./

RUN echo "$ENV" && poetry version \
  && poetry install \
    $(if [ "$ENV" = 'production' ]; then echo '--no-dev'; fi) \
    --no-interaction --no-ansi \
  # Upgrading pip, it is insecure, remove after `pip@21.1`
  && poetry run pip install -U pip \
  # Cleaning poetry installation's cache for production:
  && if [ "$ENV" = 'production' ]; then rm -rf /var/cache/pypoetry; fi


COPY . .
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
