from src.constants.prompt import template
from langchain_core.messages import AIMessage
from langchain.tools import StructuredTool
from langchain_core.runnables import Runnable
from langchain_core.messages import BaseMessage
from langchain_core.language_models.base import LanguageModelInput
from langchain_core.messages import ToolMessage
from src.utils import logger
import json
import re


_THINK_RE = re.compile(r"<think>.*?</think>", flags=re.DOTALL)
async def generate(llm_with_tools, tools: dict[str, StructuredTool], question: str):
    try:
        # 0) Tạo conversation
        messages = template.format_messages(question=question)

        # 1) Ask LLM for tool call
        ai_msg = await llm_with_tools.ainvoke(messages)
        messages.append(ai_msg)

        # 2) Thực thi tool_calls nếu có
        tool_calls = ai_msg.additional_kwargs.get("tool_calls", [])
        for tool_call in tool_calls:
            print(tool_call) # {'index': 0, 'id': '994979245', 'function': {'arguments': '{"user_input": "What do beetles eat?", "top_k": 3, "with_score": false}', 'name': 'search_docs'}, 'type': 'function'}
            name = tool_call["function"]["name"].lower()
            if name not in tools:
                raise ValueError(f"Unknown tool: {name}")
            tool_inst = tools[name]

            # parse JSON arguments
            payload = json.loads(tool_call["function"]["arguments"])
            result = tool_inst.invoke(payload)
            print(f"Result {name}:", result)
            messages.append(
                ToolMessage(
                    content=result,
                    tool_call_id=tool_call.get("id")
                )
            )

        # 3) Ask LLM final answer
        raw_resp = await llm_with_tools.ainvoke(messages)
        content_resp = raw_resp.content
        final_resp  = _THINK_RE.sub("", content_resp).strip()
        return final_resp

    except Exception as e:
        logger.error(f"Error in generate(): {e}")
        raise

async def generate_stream(
    llm_with_tools,
    tools: dict,
    question: str
):
    try:
        # 0) Tạo conversation
        messages = template.format_messages(question=question)

        # 1) Ask LLM for tool call
        ai_msg = await llm_with_tools.ainvoke(messages)
        messages.append(ai_msg)

        # 2) Thực thi tool_calls nếu có
        tool_calls = ai_msg.additional_kwargs.get("tool_calls", [])
        for tool_call in tool_calls:
            name = tool_call["function"]["name"].lower()
            if name not in tools:
                raise ValueError(f"Unknown tool: {name}")
            tool_inst = tools[name]

            # parse JSON arguments
            payload = json.loads(tool_call["function"]["arguments"])
            for call_args in payload.get("tool_calls", []):
                # invoke StructuredTool
                output = tool_inst.invoke(call_args)
                messages.append(
                    ToolMessage(
                        content=output,
                        tool_call_id=tool_call.get("id")
                    )
                )

        # 4) Stream the LLM’s final answer
        async for chunk in llm_with_tools.astream(messages):
            yield chunk.content

    except Exception as e:
        logger.error("Error in generate_stream():", e)
        raise