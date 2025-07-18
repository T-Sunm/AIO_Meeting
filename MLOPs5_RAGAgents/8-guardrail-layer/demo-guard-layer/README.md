# Welcome to demo about the lesson 6 - RAG - Observable Layer

## Setup

To run this demo, please install uv via [docs](https://docs.astral.sh/uv/getting-started/installation/)

Then run,

```bash
cd demo-guardrail-layer && \
uv venv && \
source .venv/bin/activate && \
uv sync --active
```

You need to initialize a OpenAI API Key and fill it to a file named `.env` with same format to file `sample.env`

## To run demo

### Step 1: Run RAG service with prompt from Langfuse

```bash
uv run run.py
```

### Step 2: Send API to test Q&A Chatbot

Go to `http://localhost:8055/docs` and test