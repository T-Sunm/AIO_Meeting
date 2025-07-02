from src.services.embeddings import EmbeddingService
from src.settings import SETTINGS
from langchain_chroma import Chroma  # Nếu bạn dùng langchain.vectorstores thì sửa lại import
from langchain.schema.document import Document

class ChromaClientService:
    def __init__(self):
        self.client = None
        self.collection = None
        self.embedding_service = EmbeddingService()

    def _connect(self):
        self.client = Chroma(
            collection_name=SETTINGS.CHROMA_COLLECTION_NAME,
            persist_directory=SETTINGS.CHROMA_PERSIST_DIRECTORY,
            embedding_function=self.embedding_service,
        )

    def retrieve_vector(self, question: str, top_k: int = 3, with_score: bool = False, metadata_filter: dict = {}):
        """
        Truy vấn vector database để lấy các văn bản gần nhất theo ngữ nghĩa.
        
        Args:
            question (str): câu hỏi đầu vào
            top_k (int): số kết quả muốn truy vấn
            with_score (bool): có muốn trả về điểm similarity không
            metadata_filter (dict): lọc theo metadata nếu cần (VD: {"source": "news"})
        
        Returns:
            list[Document] hoặc list[(Document, float)] nếu with_score=True
        """
        if self.client is None:
            raise ValueError("Chroma client is not initialized. Please connect to the database first.")

        if with_score:
            results = self.client.similarity_search_with_score(
                question,
                k=top_k,
                filter=metadata_filter
            )
            for doc, score in results:
                print(f"[Score={score:.4f}] {doc.page_content} [{doc.metadata}]")
        else:
            results = self.client.similarity_search(
                question,
                k=top_k,
                filter=metadata_filter
            )
            for doc in results:
                print(f"* {doc.page_content} [{doc.metadata}]")

        return results


client = ChromaClientService()
client._connect()
results = client.retrieve_vector(
    question="What is instruction tuning in LLM ?",
    top_k=2,
    with_score=True
)

print(results)