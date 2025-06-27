from airflow import DAG
from airflow.operators.python import PythonOperator, task
from airflow.utils.dates import days_ago
from datetime import timedelta
import yaml
import pandas as pd
import numpy as np
import os
from pathlib import Path
import json
import wget
from plugins.jobs.download import file_links
from plugins.utils import check_src_data

dataset_folder = os.getenv("INLINE_DATA_VOLUME")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

@task()
def start_task():
    """Downloads papers if they don't exist in the dataset folder."""
    folder_path = str(dataset_folder)
    os.makedirs(folder_path, exist_ok=True)
    
    for file_link in file_links:
        if not check_src_data(file_link):
            print(f"Downloading {file_link['title']}...")
            wget.download(file_link["url"], out=os.path.join(folder_path, f"{file_link['title']}.pdf"))
        else:
            print(f"File {file_link['title']}.pdf already exists, skipping download.")
    
    return {"status": "completed", "folder_path": folder_path}

# Create DAG
with DAG(
    'ingest_data',
    default_args=default_args,
    description='A DAG to ingest data',
    schedule_interval=None,
) as dag:
    data = start_task()
