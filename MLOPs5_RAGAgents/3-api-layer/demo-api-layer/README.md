# Welcome to demo about the lesson 3 - RAG - API Layer

## Setup

To run this demo, please install uv via [docs](https://docs.astral.sh/uv/getting-started/installation/)

Then run,

```bash
cd demo-api-layer && \
uv venv && \
/bin/activate && \
uv sync --active
```

You need to initialize a OpenAI API Key and fill it to a file named `.env` with same format to file `sample.env`

## To run the demo

```bash
uv run run.py
```

## To run a REST API

```bash
curl -X 'POST' \
  'http://localhost:8000/v1/rest-retrieve/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_input": "What do beetles eat?"
}'
```

## To run a SSE API

```bash
curl -X 'POST' \
  'http://localhost:8000/v1/sse-retrieve/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_input": "What do beetles eat?"
}'
```

## To run a WS API

Go to `localhost:8000/v1/ws-retrieve/` and typing some questions and click `send` button.
