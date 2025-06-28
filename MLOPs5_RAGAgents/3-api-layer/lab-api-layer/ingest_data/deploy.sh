#!/bin/bash

# Define directories
AIRFLOW_HOME="./airflow"
SOURCE_DIR="."

# Clean up existing directories
echo "Cleaning up existing directories..."
rm -rf "$AIRFLOW_HOME/dags"
rm -rf "$AIRFLOW_HOME/plugins"
rm -rf "$AIRFLOW_HOME/config"
rm -rf "$AIRFLOW_HOME/logs"

# Create fresh directories in Airflow
echo "Creating fresh directories..."
mkdir -p "$AIRFLOW_HOME/dags"
mkdir -p "$AIRFLOW_HOME/plugins"
mkdir -p "$AIRFLOW_HOME/config"
mkdir -p "$AIRFLOW_HOME/logs"

# Copy DAG files
echo "Copying DAG files..."
cp -rv "$SOURCE_DIR/dags"/*.py "$AIRFLOW_HOME/dags/"

# Copy plugin files
echo "Copying plugin files..."
cp -rv "$SOURCE_DIR/plugins" "$AIRFLOW_HOME/"

# Copy config files
echo "Copying config files..."
cp -rv "$SOURCE_DIR/config"/*.yaml "$AIRFLOW_HOME/config/" 2>/dev/null || echo "No config files to copy"

# Copy requirements file
echo "Copying requirements file..."
cp -v "$SOURCE_DIR/requirements.txt" "$AIRFLOW_HOME/"

# Clean up Docker resources (optional)
echo "Cleaning up Docker resources..."
cd "$AIRFLOW_HOME"
docker compose down -v
docker compose rm -f -s -v
docker volume prune -f

echo "Deployment completed!"

# Uncomment below lines if you want to automatically start Airflow
# echo "Starting Airflow containers..."
# docker compose build --no-cache
# docker compose up -d

# echo "Airflow is starting up. Please wait a few minutes for all services to be ready."
# echo "You can access the Airflow UI at http://localhost:8080"