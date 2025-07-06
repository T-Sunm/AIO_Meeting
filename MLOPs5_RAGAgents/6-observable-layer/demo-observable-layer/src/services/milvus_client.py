import json
from pymilvus import Collection, connections, utility
from src.services.embeddings import EmbeddingService


class MilvusClientService:
    def __init__(
        self, 
        host: str = "localhost", 
        port: str = "19530", 
        collection_name: str = "langchain_docs"
    ):
        self.host = host
        self.port = port
        self.collection_name = collection_name
        self.client = None
        self.collection = None
        self._connect()
        self.embedding_service = EmbeddingService()

    def _connect(self):
        connections.connect(host=self.host, port=self.port)
        if not utility.has_collection(self.collection_name):
            raise ValueError(f"Collection '{self.collection_name}' does not exist.")
        self.collection = Collection(self.collection_name)
        self.collection.load()

    def retrieve_vector(
        self, 
        question: str, 
        anns_field: str = "embedding",
        output_field: str = "text",
        limit: int = 10,
    ):
        """Retrieve documents based on the question using vector search."""
        if not self.collection:
            raise ValueError("Collection is not initialized. Please check the connection.")
        
        query_vector = self.embedding_service.embed_text(question)
        responses = self.collection.search(
            anns_field=anns_field,
            data=[query_vector],
            limit=limit,
            param={"metric_type": "L2", "params": {"nprobe": 10}},
            output_fields=[output_field],
        )
        retrieved_docs = [hit.entity[output_field] for hits in responses for hit in hits] # type: ignore
        return json.dumps(retrieved_docs)