from src.llm import llm
from src.tools import search_tool
from src.prompt import template
from langchain_core.messages import AIMessage
from langchain_core.tracers import ConsoleCallbackHandler
from src.settings import SETTINGS
from langchain.globals import set_verbose

set_verbose(True)


llm_with_tools = llm.bind_tools([search_tool])

def generate_response(question: str):
  """Generate a response to a question using the LLM with tools."""
  # Format the messages using the template and the question
  messages = template.format_messages(question=question)

  # Create an AI message using the LLM with tools
  ai_msg = llm_with_tools.invoke(messages)
  messages.append(ai_msg)

  # If the AI message contains tool calls, invoke the tools and append their responses
  if isinstance(ai_msg, AIMessage) and hasattr(ai_msg, "tool_calls"):
    for tool_call in ai_msg.tool_calls:
      # Parse message to arguments of the function calling
      selected_tool = {search_tool.name: search_tool}[
          tool_call["name"].lower()]
      tool_msg = selected_tool.invoke(tool_call)
      messages.append(tool_msg)

  # Finally, get response by invoking the LLM with the all messages
  # Currently, list of messages includes:
  # 1. User question
  # 2. AI message with tool calls (if any)
  # 3. Tool responses (if any)
  if SETTINGS.DEBUG_MODE:
    response = llm_with_tools.invoke(
        messages, config={'callbacks': [ConsoleCallbackHandler()]})
  else:
    response = llm_with_tools.invoke(messages)
  return response.content
