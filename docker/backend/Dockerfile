# Pull base image
FROM python:3.9-alpine
MAINTAINER Rafal Jusiak <kontakt@rafaljusiak.pl>

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# Install required packages
RUN apk update && apk add --no-cache coreutils build-base postgresql-dev libffi-dev curl libxml2

# Set work directory
WORKDIR /app

# Copy project
COPY . /app/

# Install project depencencies
RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt
