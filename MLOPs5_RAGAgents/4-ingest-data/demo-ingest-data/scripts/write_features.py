
from feast import FeatureStore
import pandas as pd
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

store = FeatureStore("../feature_store")

df = pd.read_parquet("rag-mini-wikipedia-embeddings-03.parquet")
df.rename(columns={"passage": "text"}, inplace=True)
df["id"] = df.index

store.write_to_online_store(feature_view_name="docs_embeddings", df=df)