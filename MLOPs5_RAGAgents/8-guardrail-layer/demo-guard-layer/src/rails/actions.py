from typing import Optional
from nemoguardrails.actions import action
from src.services.rag import Rag

# Global variable to cache the QA chain
rag_service = None

def init():
    """
    Initialize the Rag service and set it as a global variable.
    This function should be called at the start of the application.
    """
    global rag_service
    rag_service = Rag()
    print("Rag service initialized.")

async def get_query_response(rag_service: Rag, query: str):
    """
    Function to query based on the QA chain and query string passed in.
    """
    print(f"Querying with: {query}")
    result = await rag_service.generator_service.generate(query)
    print(f"Query result: {result}")
    return result

@action(is_system_action=True)
async def user_query(context: Optional[dict] = None):
    """
    Function to invoke the QA chain to query user message.
    """
    if not context or "user_message" not in context:
        return "No user message provided in context."
    
    user_message = context.get("user_message")
    print('user_message is ', user_message)
    
    if not user_message:
        return "User message is empty."

    rag_service = init()
    if rag_service is None:
        return "Rag service is not initialized."
    
    return await get_query_response(rag_service, user_message)