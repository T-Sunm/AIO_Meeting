from src.constants.prompt import template
from langchain_core.messages import AIMessage
from langchain.tools import Tool
from langchain_core.runnables import Runnable
from langchain_core.messages import BaseMessage
from langchain_core.language_models.base import LanguageModelInput
from typing import AsyncGenerator


async def generate(llm_with_tools: Runnable[LanguageModelInput, BaseMessage], tool: Tool, question: str):
    """Generate a response to a question using the LLM with tools."""
    # Format the messages using the template and the question
    messages = template.format_messages(question=question)
    
    # Create an AI message using the LLM with tools
    ai_msg = await llm_with_tools.ainvoke(messages)
    messages.append(ai_msg)
    
    # If the AI message contains tool calls, invoke the tools and append their responses
    if isinstance(ai_msg, AIMessage) and hasattr(ai_msg, "tool_calls"):
        for tool_call in ai_msg.tool_calls:
            # Parse message to arguments of the function calling
            selected_tool = {"search_docs": tool}[tool_call["name"].lower()]
            tool_msg = await selected_tool.ainvoke(tool_call)
            messages.append(tool_msg)
    
    # Finally, get response by invoking the LLM with the all messages
    # Currently, list of messages includes:
    # 1. User question  
    # 2. AI message with tool calls (if any) 
    # 3. Tool responses (if any)
    response = await llm_with_tools.ainvoke(messages)
    return response.content

async def generate_stream(
    llm_with_tools: Runnable[LanguageModelInput, BaseMessage],
    tool: Tool,
    question: str
) -> AsyncGenerator[str, None]:
    """Generate a response to a question using the LLM with tools (streamed)."""
    messages = template.format_messages(question=question)
    
    # Create an AI message using the LLM with tools
    ai_msg = await llm_with_tools.ainvoke(messages)
    messages.append(ai_msg)
    
    # If the AI message contains tool calls, invoke the tools and append their responses
    if isinstance(ai_msg, AIMessage) and hasattr(ai_msg, "tool_calls"):
        for tool_call in ai_msg.tool_calls:
            # Parse message to arguments of the function calling
            selected_tool = {tool.name: tool}[tool_call["name"].lower()]
            tool_msg = await selected_tool.ainvoke(tool_call)
            messages.append(tool_msg)
            
    async for message in llm_with_tools.astream(messages):
        yield str(message.content)