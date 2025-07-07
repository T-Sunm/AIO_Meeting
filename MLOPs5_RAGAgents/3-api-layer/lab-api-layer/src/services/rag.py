from src.services.generator import GeneratorService
from langchain.tools import StructuredTool
from langchain_openai import ChatOpenAI
from src.settings import SETTINGS
from src.services.chroma_client import ChromaClientService
from src.schemas.retrieval import SearchArgs
from src.utils import logger
from langfuse import observe
from langfuse.langchain import CallbackHandler

class Rag:
    def __init__(self):
        self.llm = ChatOpenAI(
            openai_api_base="http://127.0.0.1:1234/v1",
            temperature=SETTINGS.LLMs_TEMPERATURE,
            openai_api_key="dummy",
            streaming=True,
        )
        self.chroma_client = ChromaClientService()
        self.chat_history: list[dict] = []
        self.langfuse_handler = CallbackHandler()
        # Define search tool
        self.search_tool = StructuredTool.from_function(
            name="search_docs",
            description=(
                "Retrieve documents from Chroma.\n"
                "Args:\n"
                "    question (str): the question.\n"
                "    top_k (int): the number of documents to retrieve.\n"
                "    with_score (bool): whether to include similarity scores.\n"
                "    metadata_filter (dict): filter by metadata.\n"
            ),
            func=self.chroma_client.retrieve_vector,
            args_schema=SearchArgs
        )

        # Define tools dictionary
        self.tools = {
            "search_docs": self.search_tool
        }
        
        # Bind tools to LLM
        self.llm_with_tools = self.llm.bind_tools(list(self.tools.values())).with_config({
            "callbacks": [self.langfuse_handler]
        })

        # Initialize generator service
        self.generator_service = GeneratorService(
            llm_with_tools=self.llm_with_tools,
            tools=self.tools,
            langfuse_handler=self.langfuse_handler
        )

    @observe(name="rag-service")
    async def get_response(self, question: str):
        self.chat_history.append({"role": "user", "content": question})
        response = await self.generator_service.generate(
            question=question,
            chat_history=self.chat_history
        )
        self.chat_history.append({"role": "assistant", "content": response})
        logger.info(f"Chat history length: {len(self.chat_history)}")
        return response

    async def get_sse_response(self, question: str):
        async for message in self.generator_service.generate_stream(
            question=question,
        ):
            yield f"event: responseUpdate\ndata: {message}\n\n"