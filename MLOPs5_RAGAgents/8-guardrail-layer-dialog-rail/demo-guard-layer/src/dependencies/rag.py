from fastapi import Request
from src.services.rag import Rag


def get_rag_service(request: Request) -> Rag:
    return request.app.state.rag_service


def get_rails(request: Request):
    """
    Dependency to get the Rails instance from the FastAPI app state.
    """
    return request.app.state.rails
