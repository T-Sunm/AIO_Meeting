from minio import Minio
from minio.error import S3Error
from io import BytesIO
import pickle
import os
import logging
from airflow.models import Variable


MINIO_ENDPOINT = "milvus-minio:9000"
MINIO_ACCESS_KEY = Variable.get("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = Variable.get("MINIO_SECRET_KEY")


def get_info_from_minio(s3_path: str):
    s3_path = s3_path.replace("s3://", "")
    s3_bucket, s3_key = s3_path.split("/", 1)
    return s3_bucket, s3_key


def upload_to_minio(data, s3_path: str):
    s3_bucket, s3_key = get_info_from_minio(s3_path)
    print(f"Bucket: {s3_bucket}")
    print(f"Key: {s3_key}")
    client = Minio(
        MINIO_ENDPOINT,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=False,  # Set to True if using HTTPS
    )
    
    found = client.bucket_exists(s3_bucket)
    if not found:
        client.make_bucket(s3_bucket)
        print("Created bucket", s3_bucket)
    else:
        print("Bucket", s3_bucket, "already exists")
    
    buffer = BytesIO()
    pickle.dump(data, buffer)
    buffer.seek(0)
    try:
        client.put_object(
            bucket_name=s3_bucket,
            object_name=s3_key,
            data=buffer,
            length=buffer.getbuffer().nbytes,
        )
    except S3Error as e:
        logger.error(f"Failed to upload to MinIO: {e}")
        raise


def download_from_minio(s3_path: str):
    s3_bucket, s3_key = get_info_from_minio(s3_path)
    client = Minio(
        MINIO_ENDPOINT,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=False,  # Set to True if using HTTPS
    )
    buffer = BytesIO()
    try:
        response = client.get_object(bucket_name=s3_bucket, object_name=s3_key)
        buffer.write(response.read())
        buffer.seek(0)
        return pickle.load(buffer)
    except S3Error as e:
        logger.error(f"Failed to download from MinIO: {e}")
        raise


def get_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger(__name__)


logger = get_logger()