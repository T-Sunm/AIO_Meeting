from langchain_core.messages import AIMessage
from langchain.tools import Tool
from langchain_core.runnables import Runnable
from langchain_core.messages import BaseMessage
from langchain_core.language_models.base import LanguageModelInput
from typing import AsyncGenerator
from langfuse import observe, get_client
from typing import Optional
from langfuse.langchain import CallbackHandler
from langchain_community.cache import RedisSemanticCache
from langchain_openai import OpenAIEmbeddings
from langchain_core.outputs import Generation
from nemoguardrails import LLMRails
from langchain.globals import set_llm_cache

        
class GeneratorService:
    def __init__(
        self, 
        llm_with_tools: Runnable[LanguageModelInput, BaseMessage],
        tool: Tool,
    ):
        self.llm_with_tools = llm_with_tools
        self.tool = tool
        self.langfuse = get_client()
        self.prompt = self.langfuse.get_prompt(
            "rag-service",
            label="production",
            type="chat",
        )
        self.langfuse_handler = CallbackHandler()
        self.semantic_cache = RedisSemanticCache(
            redis_url="redis://localhost:6378",
            embedding=OpenAIEmbeddings()
        )
        set_llm_cache(self.semantic_cache)
        
    
    async def _create_message(self, question: str):
        """Create a message with the question."""
        messages = self.prompt.get_langchain_prompt(question=question)
        
        # Create an AI message using the LLM with tools
        ai_msg = await self.llm_with_tools.ainvoke(messages)
        messages.append(ai_msg) # type: ignore
        
        # If the AI message contains tool calls, invoke the tools and append their responses
        if isinstance(ai_msg, AIMessage) and hasattr(ai_msg, "tool_calls"):
            for tool_call in ai_msg.tool_calls:
                # Parse message to arguments of the function calling
                selected_tool = {self.tool.name: self.tool}[tool_call["name"].lower()]
                tool_msg = await selected_tool.ainvoke(tool_call)
                messages.append(tool_msg)
                
        return messages
    
    @observe(name="rag-service")
    async def generate(
        self, 
        question: str,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None,
        rails_service: Optional[LLMRails] = None,
    ):
        """Generate a response to a question using the LLM with tools."""
        if session_id or user_id:
            # If session_id or user_id is provided, update the current trace
            # This is useful for tracking user sessions in Langfuse
            # and associating the trace with the user
            # This will also create a new trace if it does not exist
            self.langfuse.update_current_trace(
                session_id=session_id,
                user_id=user_id,
            )
        
        if rails_service:
            guardrails_result = await rails_service.generate_async(prompt=question)
            print(f"Guardrails result: {guardrails_result}")
            if "sorry" not in str(guardrails_result):
                # If the guardrails result does not contain "not", return the result
                # This means the guardrails did not block the response
                return guardrails_result
            
        if self.semantic_cache:
            # Check if the question is already cached
            cached_response = self.semantic_cache.lookup('rag-service', question)
            if cached_response:
                return cached_response[0].text
            
        print(f"Generating response for question: {question}")
        response = await self.get_response(question)
        if hasattr(response, 'content'):
            response = response.content
            
        print(f"Generated response: {response}")
        
        if self.semantic_cache and response:
            # Cache the response if semantic cache is available
            self.semantic_cache.update('rag-service', question, [
                Generation(
                    text=str(response), 
                )]
            )
            
        return response
    
    async def get_response(
        self,
        question: str,
    ):
        messages = await self._create_message(question)
        # Finally, get response by invoking the LLM with the all messages
        # Currently, list of messages includes:
        # 1. User question  
        # 2. AI message with tool calls (if any) 
        # 3. Tool responses (if any)
        response = await self.llm_with_tools.ainvoke(messages, config={"callbacks": [self.langfuse_handler]})
        return response
        
    async def generate_stream(self, question: str) -> AsyncGenerator[str, None]:
        """Generate a response to a question using the LLM with tools (streamed)."""
        messages = await self._create_message(question)
        
        async for message in self.llm_with_tools.astream(messages):
            yield str(message.content)