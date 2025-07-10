from fastapi import APIRouter
from src.routers import retrieval

api_router = APIRouter()
api_router.include_router(
    retrieval.router, prefix="/retrieve", tags=["REST API Retriever"]
)