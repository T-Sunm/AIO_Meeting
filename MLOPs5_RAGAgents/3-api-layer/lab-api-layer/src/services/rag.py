from src.services import generate, generate_stream, retrieve
from langchain.tools import StructuredTool, Tool
from langchain_openai import ChatOpenAI
from src.settings import SETTINGS
from src.constants.enum import LLMModel
from typing import Optional
from langchain.callbacks.base import AsyncCallbackHandler
from src.services.chroma_client import ChromaClientService
from src.schemas.retrieval import SearchArgs
from src.utils import logger
class Rag:
  def __init__(self, llm_callback: Optional[AsyncCallbackHandler] = None):
    self.llm = ChatOpenAI(
        openai_api_base="http://127.0.0.1:1234/v1",
        temperature=SETTINGS.LLMs_TEMPERATURE,
        openai_api_key="dummy",
        streaming=True,
        callbacks=[llm_callback] if llm_callback else None,
    )
    self.chroma_client = ChromaClientService()
    
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

    self.tools = {
            "search_docs": self.search_tool
      }
    self.llm_with_tools = self.llm.bind_tools(list(self.tools.values()))

  async def get_response(self, question: str):
    response = await generate(
        llm_with_tools=self.llm_with_tools,
        tools=self.tools,
        question=question,
    )
    return response

  async def get_sse_response(self, question: str):
    async for message in generate_stream(
        llm_with_tools=self.llm_with_tools,
        tools=self.tools,
        question=question,
    ):
      yield f"event: responseUpdate\ndata: {message}\n\n"
