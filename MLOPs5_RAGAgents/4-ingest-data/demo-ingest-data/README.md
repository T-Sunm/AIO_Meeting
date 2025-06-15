# Welcome to demo about the lesson 4 - RAG - Ingest Data

## Setup

To run this demo, please install uv via [docs](https://docs.astral.sh/uv/getting-started/installation/)

Then run,
```bash
cd demo && \
uv venv && \
source .venv/bin/activate && \
uv sync --active
```

You need to initialize a OpenAI API Key and fill it to a file named `.env` with same format to file `sample.env`


## To setup infra

### For Airflow/Milvus/Minio
```bash
cd infra && 
docker compose up -d
```

### For run DAG

- Go to http://localhost:8080
- Find DAG `ingest_pipeline_with_minio_and_feature_store` and trigger

### For run service 

```bash
uv run run.py
```

### For Feast UI
```bash
cd feature_store && feast ui 
```

Then go to http://0.0.0.0:8888/

### For Milvus UI

- Go to http://localhost:8000/