# Version Airflow et Python
ARG AIRFLOW_VERSION=2.9.2
ARG PYTHON_VERSION=3.10

# Image officielle Airflow
FROM apache/airflow:${AIRFLOW_VERSION}-python${PYTHON_VERSION}

# Répertoire principal Airflow
ENV AIRFLOW_HOME=/opt/airflow

# Je copie les dépendances
COPY requirements.txt /

# Installer dépendances
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt