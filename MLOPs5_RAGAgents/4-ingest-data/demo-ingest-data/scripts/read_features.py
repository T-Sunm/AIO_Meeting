from feast import FeatureStore
import warnings
from sentence_transformers import SentenceTransformer

warnings.filterwarnings("ignore")

model = SentenceTransformer("all-MiniLM-L6-v2")
store = FeatureStore("../feature_store")
query = "What do beetles eat?"

embedding = model.encode(query).tolist()
print("Query embedding:", len(embedding))

context_data = store.retrieve_online_documents_v2(
    features=[
        "docs_embeddings:embedding",
        "docs_embeddings:id",
        "docs_embeddings:text",
    ],
    query=embedding,
    top_k=3,
    distance_metric="COSINE",
).to_df()

print(context_data)