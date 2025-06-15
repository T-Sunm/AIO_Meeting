import pandas as pd
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from plugins.jobs.utils import upload_to_minio, logger


def load_and_chunk(input_uri: str, output_uri: str):
    df = pd.read_parquet(input_uri)
    docs = [Document(page_content=p) for p in df.passage.values]
    splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=100)
    splits = splitter.split_documents(docs)
    upload_to_minio(splits, output_uri)
    logger.info(f"Uploaded chunks to MinIO: {input_uri}/{output_uri}")
    