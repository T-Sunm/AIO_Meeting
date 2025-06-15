from src.constants.prompt import system_prompt
from langchain_core.messages import AIMessage
from langchain.tools import Tool
from langchain_core.runnables import Runnable
from langchain_core.messages import BaseMessage
from langchain_core.language_models.base import LanguageModelInput
from typing import AsyncGenerator

        
class GeneratorService:
    def __init__(
        self, 
        llm_with_tools: Runnable[LanguageModelInput, BaseMessage],
        tool: Tool,
    ):
        self.llm_with_tools = llm_with_tools
        self.tool = tool
        
        
    async def _create_message(self, question: str):
        """Create a message with the question."""
        messages = system_prompt.format_messages(question=question)
        
        # Create an AI message using the LLM with tools
        ai_msg = await self.llm_with_tools.ainvoke(messages)
        messages.append(ai_msg)
        
        # If the AI message contains tool calls, invoke the tools and append their responses
        if isinstance(ai_msg, AIMessage) and hasattr(ai_msg, "tool_calls"):
            for tool_call in ai_msg.tool_calls:
                # Parse message to arguments of the function calling
                selected_tool = {self.tool.name: self.tool}[tool_call["name"].lower()]
                tool_msg = await selected_tool.ainvoke(tool_call)
                messages.append(tool_msg)
                
        return messages
    
    
    async def generate(self, question: str):
        """Generate a response to a question using the LLM with tools."""
        messages = await self._create_message(question)
        
        # Finally, get response by invoking the LLM with the all messages
        # Currently, list of messages includes:
        # 1. User question  
        # 2. AI message with tool calls (if any) 
        # 3. Tool responses (if any)
        response = await self.llm_with_tools.ainvoke(messages)
        return response.content
        
    async def generate_stream(self, question: str) -> AsyncGenerator[str, None]:
        """Generate a response to a question using the LLM with tools (streamed)."""
        messages = await self._create_message(question)
        
        async for message in self.llm_with_tools.astream(messages):
            yield str(message.content)