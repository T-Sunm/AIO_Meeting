from fastapi import APIRouter, Depends, status
from src.dependencies.rag import get_rag_service, get_rails
from src.schemas.retrieval import RetrievalInput
from src.services.rag import Rag
from nemoguardrails import LLMRails

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=str,
)
async def retrieve_restaurants(
    input: RetrievalInput,
    rag_service: Rag = Depends(get_rag_service),
    rails_service: LLMRails = Depends(get_rails),
):
    response = await rag_service.get_embeddings_response(
        question=input.user_input,
        session_id=input.session_id,
        user_id=input.user_id,
        rails_service=rails_service,
    )

    return response