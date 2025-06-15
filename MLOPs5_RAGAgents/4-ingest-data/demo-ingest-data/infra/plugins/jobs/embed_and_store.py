from plugins.jobs.utils import download_from_minio

import pandas as pd
from sentence_transformers import SentenceTransformer

def embed_and_store(input_uri: str):
    from feast import FeatureStore
    store = FeatureStore("plugins/config")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    splits = download_from_minio(input_uri)

    # Embed
    texts = [doc.page_content for doc in splits]
    df = pd.DataFrame({
        "passage": texts,
        "event_timestamp": pd.Timestamp.now(tz='UTC')
    })
    df['embedding'] = df['passage'].apply(lambda x: model.encode(x).tolist())
    df["id"] = df.index

    # Insert into Milvus via Feature Store
    store.write_to_online_store(feature_view_name="docs_embeddings", df=df)