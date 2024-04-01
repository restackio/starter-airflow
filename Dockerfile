ARG RESTACK_PRODUCT_VERSION=2.8.0

FROM apache/airflow:${RESTACK_PRODUCT_VERSION}

ENV DBT_PROJECT_DIR=/opt/airflow/dbt_project
ENV DBT_PROFILE_DIR=/opt/airflow/dbt_project/profiles.yml

RUN mkdir -p dags && \
    mkdir -p config && \
    mkdir -p logs && \
    mkdir -p plugins

COPY --chown=airflow:root dags/ /opt/airflow/dags
COPY --chown=airflow:root config/ /opt/airflow/config
COPY --chown=airflow:root plugins/ /opt/airflow/plugins
COPY --chown=airflow:root dbt_project/ "$DBT_PROJECT_DIR"


COPY requirements.txt /
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt
RUN cd /opt/airflow/dbt_project && dbt deps
