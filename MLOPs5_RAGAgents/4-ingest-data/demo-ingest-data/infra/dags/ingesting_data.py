from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from plugins.jobs.load_and_chunk import load_and_chunk
from plugins.jobs.embed_and_store import embed_and_store

# Settings
DATASET_PATH = "hf://datasets/rag-datasets/rag-mini-wikipedia/data/passages.parquet/part.0.parquet"
MINIO_ENDPOINT = "http://localhost:9000"
MINIO_ACCESS_KEY = Variable.get("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = Variable.get("MINIO_SECRET_KEY")
MINIO_PATH = "rag-pipeline/chunks.pkl"


def load_and_chunk_task(**kwargs):
    load_and_chunk(
        input_uri=DATASET_PATH,
        output_uri=MINIO_PATH,
    )
    return MINIO_PATH


def embed_and_store_task(**kwargs):
    input_uri = kwargs['ti'].xcom_pull(task_ids='load_and_chunk_task')
    embed_and_store(
        input_uri=input_uri,
    )


with DAG(
    dag_id="ingest_pipeline_with_minio_and_feature_store",
    start_date=datetime(2023, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    load_and_chunk_op = PythonOperator(
        task_id="load_and_chunk_task",
        python_callable=load_and_chunk_task,
    )

    embed_and_store_op = PythonOperator(
        task_id="embed_and_store_task",
        python_callable=embed_and_store_task,
    )

    _ = load_and_chunk_op >> embed_and_store_op