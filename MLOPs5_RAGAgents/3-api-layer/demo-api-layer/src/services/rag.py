from src.services import retrieve, generate, generate_stream
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from src.settings import SETTINGS
from src.constants.enum import LLMModel
from typing import Optional
from langchain.callbacks.base import AsyncCallbackHandler


class Rag:
  def __init__(self, llm_callback: Optional[AsyncCallbackHandler] = None):
    self.llm = ChatOpenAI(
        openai_api_base="http://127.0.0.1:1234/v1",
        api_key=SETTINGS.OPENAI_API_KEY,
        temperature=SETTINGS.OPENAI_TEMPERATURE,
        streaming=True,
        callbacks=[llm_callback] if llm_callback else None,
    )
    self.search_tool = Tool(
        name="search_docs",
        description="Search for documents relevant to a query",
        func=retrieve,
    )
    self.llm_with_tools = self.llm.bind_tools([self.search_tool])

  async def get_response(self, question: str):
    response = await generate(
        llm_with_tools=self.llm_with_tools,
        tool=self.search_tool,
        question=question,
    )
    return response

  async def get_sse_response(self, question: str):
    async for message in generate_stream(
        llm_with_tools=self.llm_with_tools,
        tool=self.search_tool,
        question=question,
    ):
      yield f"event: responseUpdate\ndata: {message}\n\n"
