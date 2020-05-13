# Pull base image
FROM python:3.8-alpine
MAINTAINER Rafal Jusiak <kontakt@rafaljusiak.pl>

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_PATH=/opt/poetry \
    VENV_PATH=/opt/venv

ENV PATH="$POETRY_PATH/bin:$VENV_PATH/bin:$PATH"

# Install required packages
RUN apk update && apk add --no-cache coreutils build-base postgresql-dev libffi-dev curl

# Set work directory
WORKDIR /app

# Install poetry and configure venv
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
RUN mv /root/.poetry $POETRY_PATH
RUN python -m venv $VENV_PATH
RUN poetry config virtualenvs.create false

# Copy project
COPY . /app/

# Install project depencencies
RUN poetry install --no-interaction --no-ansi -vvv
