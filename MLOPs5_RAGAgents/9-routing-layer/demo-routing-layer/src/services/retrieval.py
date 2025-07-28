from src.utils import logger
from sentence_transformers import SentenceTransformer
from feast import FeatureStore
import json


class RetrievalService:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.store = FeatureStore("src")

    def retrieve_vector(self, question: str):
        """Retrieve documents based on the question using vector search."""
        try:
            embedding = self.model.encode(question).tolist()
            retrieved_docs = self.store.retrieve_online_documents_v2(
                features=[
                    "docs_embeddings:passage",
                ],
                query=embedding,
                top_k=3,
                distance_metric="COSINE",
            ).to_df().values.tolist()
            print(f"Retrieved documents: {retrieved_docs}")
            return json.dumps(retrieved_docs, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error during vector retrieval: {e}")
            return []