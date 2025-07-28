from src.settings import SETTINGS
from langchain_openai import OpenAIEmbeddings
from src.constants.enum import LLMModel


class EmbeddingService:
    def __init__(self):
        self.embedding_model = OpenAIEmbeddings(
            model=LLMModel.OPENAI_TEXT_EMBEDDING_3_LARGE.value, 
            api_key=SETTINGS.OPENAI_API_KEY
        )

    def embed_text(self, text: str):
        """Embed a single text."""
        return self.embedding_model.embed_query(text)

    def embed_texts(self, texts: list[str]):
        """Embed a list of texts."""
        return self.embedding_model.embed_documents(texts)