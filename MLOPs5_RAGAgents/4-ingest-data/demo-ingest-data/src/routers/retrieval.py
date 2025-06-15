from fastapi import APIRouter, Depends, status
from src.dependencies.rag import get_rag_service
from src.schemas.retrieval import RetrievalInput
from src.services.rag import Rag

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=str,
)
async def retrieve_restaurants(
    input: RetrievalInput,
    rag_service: Rag = Depends(get_rag_service),
):
    response = await rag_service.get_embeddings_response(
        question=input.user_input,
    )

    return response