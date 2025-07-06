from src.constants.prompt import temp_userinput, temp_rag
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
async def generate(llm_with_tools, tools: dict[str, StructuredTool], question: str, chat_history: list[dict]):
    try:
        messages = temp_userinput.format_messages(question=question)
        ai_msg = await llm_with_tools.ainvoke(messages)
        chat_history.append({"role": "assistant", "content": ai_msg.content, "tool_calls": ai_msg.additional_kwargs.get("tool_calls", [])})

        # Nếu LLM không gọi tool, clean up và trả luôn
        tool_calls = ai_msg.additional_kwargs.get("tool_calls", [])
        if not tool_calls:
            return _THINK_RE.sub("", ai_msg.content or "").strip()

        # --- PHASE 2: Run tool(s) & gather context ---
        print(tool_calls)
        all_context = []
        for call in tool_calls:
            name = call["function"]["name"].lower()
            if name not in tools:
                raise ValueError(f"Unknown tool: {name}")
            tool_inst = tools[name]

            payload = json.loads(call["function"]["arguments"])
            result = tool_inst.invoke(payload)
            all_context.append(result)

            # Append ToolMessage để LLM “biết” đã chạy tool
            chat_history.append({"role": "assistant", "content": result})

        # Gộp tất cả context lại thành một string (tuỳ bạn format)
        context_str = "\n\n--- Retrieved Documents ---\n\n".join(all_context)

        # --- PHASE 3: Tái prompt bằng temp_rag ---
        prompt = temp_rag.format(
            chat_history="\n".join(f"{m['role'].capitalize()}: {m['content']}" for m in chat_history),
            question=question,
            context=context_str
        )
        rag_msgs = [{"role": "system", "content": prompt}]
        # Cuối cùng gọi LLM với template rag-prompt
        raw = await llm_with_tools.ainvoke(rag_msgs)
        answer = _THINK_RE.sub("", raw.content or "").strip()
        return answer

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
        messages = temp_userinput.format_messages(question=question)

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