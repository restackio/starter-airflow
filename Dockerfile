ARG RESTACK_PRODUCT_VERSION=2.8.0
ARG PROJECT_NAME=starter_airflow
ARG RESTACK_PATH=restack/$PROJECT_NAME
ARG BUILD_PYTHON_VERSION=3.10
ARG POETRY_VERSION=1.7.1

# Base image to install poetry and copy files
FROM python:$BUILD_PYTHON_VERSION as base
ARG RESTACK_PATH
ARG POETRY_VERSION

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=$POETRY_VERSION python3 -
ENV PATH="$POETRY_HOME/bin:$PATH"

COPY . ./$RESTACK_PATH

# Build stage to export requirements and build the module
FROM base as build
ARG RESTACK_PATH

WORKDIR $RESTACK_PATH
RUN poetry build --format wheel

# Final stage that install the module and its requirements
FROM apache/airflow:${RESTACK_PRODUCT_VERSION}

ARG PROJECT_NAME
ARG RESTACK_PATH
ARG RESTACK_PRODUCT_VERSION

USER airflow

RUN mkdir -p dags && \
    mkdir -p config && \
    mkdir -p logs && \
    mkdir -p plugins

COPY --chown=airflow:root dags/ /opt/airflow/dags
COPY --chown=airflow:root config/ /opt/airflow/config
COPY --chown=airflow:root plugins/ /opt/airflow/plugins
