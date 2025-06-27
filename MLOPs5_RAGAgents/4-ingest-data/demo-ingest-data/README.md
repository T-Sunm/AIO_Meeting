# Welcome to demo about the lesson 4 - RAG - Ingest Data

## Setup

To run this demo, please install uv via [docs](https://docs.astral.sh/uv/getting-started/installation/)

Then run,

```bash
cd demo-ingest-data && \
uv venv && \
source .venv/bin/activate && \
uv sync --active
```

You need to initialize a OpenAI API Key and fill it to a file named `.env` with same format to file `sample.env`

## To setup infra
### For Airflow/Milvus/Minio/Attu

Firstly, you need to build a custom image for Airflow
```bash
cd infra && docker build -t custom-airflow .
```

Then, run docker-compose
```bash
docker compose up -d
```

### For run DAG

- Go to http://localhost:8080
- Find DAG `ingest_pipeline_with_minio_and_feature_store` and trigger

### For Feast

Firstly, you need onboard Milvus table on Feast

```bash
cd feature_store && uv run feast apply
```

### For running service

```bash
uv run run.py
```

### For Feast UI

```bash
cd feature_store && feast ui 
```

Then go to http://0.0.0.0:8888/

### For Milvus UI (Attu)

- Go to http://localhost:8000/
