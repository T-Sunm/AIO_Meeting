#!/bin/bash

SOURCE_DIR="."
AIRFLOW_DIR="../airflow/"
DAGS_DIR="../airflow/dags/"
CONFIG_DIR="../airflow/config/"

# Copy all .py from SOURCE_DIR to DAGS_DIR
mkdir -p "$DAGS_DIR"
cp -v "$SOURCE_DIR"/*.py "$DAGS_DIR"

# Copy all .yaml from SOURCE_DIR to CONFIG_DIR
mkdir -p "$CONFIG_DIR"
cp -v "$SOURCE_DIR"/*.yaml "$CONFIG_DIR"

# Copy requirements.txt to AIRFLOW_DIR
cp -v "$SOURCE_DIR"/requirements.txt "$AIRFLOW_DIR"
