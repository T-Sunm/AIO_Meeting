# Welcome to demo about the lesson 8 - RAG - Guardrail Layer

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


## TO use dialog rails, what differences?

### 1. Use model `gpt-3.5-turbo-instruct` instead of `gpt-3.5-turbo` or `gpt-4o` family or `gpt-4.1` family.

Due to format of dialog rails, current version of nemo guardrails does not support with other models.

### 2. If using dialog rails, cannot use task `user query ` in `src/rails/config.yml`

That is trade off. If you want custom RAG, you cannot define custom task. I think that is bug of nemo guardrails.

### 3. Due to the second difference, you need to call `function calling` before running `rail_service.generate_async` in `src/services/generator.py`

### 4. In general instruction, I removed example conversation. 

If using example conversation, it will break dialog rails.