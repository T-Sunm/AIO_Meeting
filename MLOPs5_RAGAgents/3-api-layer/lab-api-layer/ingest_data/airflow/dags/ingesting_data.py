from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import os
import wget
import sys
from pathlib import Path
from airflow.decorators import task


# Add plugins directory to Python path
AIRFLOW_HOME = Path("/opt/airflow")
sys.path.append(str(AIRFLOW_HOME))
from plugins.download import file_links
from plugins.utils import check_src_data
from plugins.load_and_chunk import LoadAndChunk


dataset_folder = os.getenv("INLINE_DATA_VOLUME")
MINIO_PATH = "rag-pipeline/chunks.pkl"


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
        dest_file_path = os.path.join(folder_path, f"{file_link['title']}.pdf")
        if not check_src_data(dest_file_path):
            print(f"Downloading {file_link['title']}...")
            wget.download(file_link["url"], out=dest_file_path)
        else:
            print(f"File {file_link['title']}.pdf already exists, skipping download.")
    
    return {"status": "completed", "folder_path": folder_path}


@task()
def load_and_chunk_data():
    loader = LoadAndChunk()
    pdf_files = loader.load_dir(dataset_folder)
    chunks = loader.read_and_chunk(pdf_files)
    loader.ingest_to_minio(chunks, MINIO_PATH)
    

# Create DAG
with DAG(
    'ingest_data',
    default_args=default_args,
    description='A DAG to ingest data',
    schedule_interval=None,
) as dag:

    # Tasks
    data = start_task()
    load_and_chunk_data = load_and_chunk_data()

    # task flow
    data >> load_and_chunk_data