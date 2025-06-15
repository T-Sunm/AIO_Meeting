from src.utils import logger
from src.services.milvus_client import MilvusClientService
from src.settings import SETTINGS
from sentence_transformers import SentenceTransformer
from feast import FeatureStore
import json


class RetrievalService:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.store = FeatureStore("src")
        self.milvus_client = MilvusClientService(
            host=SETTINGS.MILVUS_HOST,
            port=SETTINGS.MILVUS_PORT,
            collection_name=SETTINGS.MILVUS_COLLECTION,
        )

    def retrieve_vector(self, question: str):
        """Retrieve documents based on the question using vector search."""
        try:
            embedding = self.model.encode(question).tolist()
            retrieved_docs = self.store.retrieve_online_documents_v2(
                features=[
                    "docs_embeddings:embedding",
                    "docs_embeddings:id",
                    "docs_embeddings:passage",
                ],
                query=embedding,
                top_k=3,
                distance_metric="COSINE",
            ).to_df().values
            return json.dumps(retrieved_docs)
        except Exception as e:
            logger.error(f"Error during vector retrieval: {e}")
            return []