from typing import Optional
from nemoguardrails.actions import action
from src.services.rag import Rag

# Global variable to cache the QA chain
rag_service = Rag()


async def get_query_response(rag_service: Rag, query: str):
    """
    Function to query based on the QA chain and query string passed in.
    """
    result = await rag_service.generator_service.get_response(query)
    return result


@action(is_system_action=True)
async def user_query(context: Optional[dict] = None):
    """
    Function to invoke the QA chain to query user message.
    """
    if not context or "user_message" not in context:
        return "No user message provided in context."

    user_message = context.get("user_message")
    print("user_message is ", user_message)

    if not user_message:
        return "User message is empty."

    return await get_query_response(rag_service, user_message)
