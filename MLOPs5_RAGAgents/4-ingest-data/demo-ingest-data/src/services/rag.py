from langchain.tools import Tool
from langchain.chat_models import init_chat_model
from src.settings import SETTINGS
from src.services.generator import GeneratorService
from src.services.retrieval import RetrievalService
from src.constants.enum import LLMModel, LLMProvider


class Rag:
    def __init__(self):
        self.llm_chat = init_chat_model(
            LLMModel.OPENAI_GPT_4O_MINI.value,
            api_key=SETTINGS.OPENAI_API_KEY,
            temperature=SETTINGS.OPENAI_TEMPERATURE,
            model_provider=LLMProvider.OPENAI.value,
        )
        
        self.retrieval_service = RetrievalService()
        self.search_tool = Tool(
            name="search_embeddings",
            description="Search for documents relevant to a query",
            func=self.retrieval_service.retrieve_vector,
        )
        self.llm_with_tools = self.llm_chat.bind_tools([self.search_tool])
                
        self.generator_service = GeneratorService(
            llm_with_tools=self.llm_with_tools,
            tool=self.search_tool,
        )
        

    async def get_embeddings_response(self, question: str):
        """Generate a response to a question using the LLM with embeddings."""
        # Use the generator service to get the response
        response = await self.generator_service.generate(question)
        return response
    