# Welcome to demo about the lesson 2 - Basic RAG pipeline

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


## To run the basic RAG pipeline

```bash
uv run main.py
```
