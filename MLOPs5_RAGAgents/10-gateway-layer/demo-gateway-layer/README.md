# Welcome to demo about the lesson 10 - RAG - Gateway Layer

## Setup

To run this demo, please install uv via [docs](https://docs.astral.sh/uv/getting-started/installation/)

Then run,

```bash
cd demo-routing-layer && \
uv venv && \
source .venv/bin/activate && \
uv sync --active
```

You need to initialize a OpenAI API Key and fill it to a file named `.env` with same format to file `sample.env`

## To run demo

### Step 1: Build the infra for LiteLLM

You need to define env in folder `infra` based on `env.example`

```bash
cd infra && docker compose up -d
```

In addition, you need to setup:
- RBAC: https://docs.litellm.ai/docs/proxy/access_control

### Step 2: Run RAG service 

```bash
uv run run.py
```

### Step 3: Send API to test Q&A Chatbot

Go to `http://localhost:8055/docs` and test