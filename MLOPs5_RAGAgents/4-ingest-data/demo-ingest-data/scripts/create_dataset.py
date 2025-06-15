from sentence_transformers import SentenceTransformer
import pandas as pd
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. Load a pretrained Sentence Transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# 2. Load the dataset
DATASET_PATH = "hf://datasets/rag-datasets/rag-mini-wikipedia/data/passages.parquet/part.0.parquet"
df = pd.read_parquet(DATASET_PATH)

docs = [Document(page_content=p) for p in df.passage.values]
splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=100)
splits = splitter.split_documents(docs)

df = pd.DataFrame({
    "passage": [doc.page_content for doc in splits],
})

# 3. Generate embeddings for the 'passage' column
df['embedding'] = df['passage'].apply(lambda x: model.encode(x).tolist())
df['event_timestamp'] = pd.Timestamp.now(tz='UTC')

# 4. Save the DataFrame with embeddings to a new Parquet file
OUTPUT_PATH = "./rag-mini-wikipedia-embeddings-03.parquet"
df.to_parquet(OUTPUT_PATH, index=False)
