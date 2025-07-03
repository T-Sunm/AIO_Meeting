from fastapi import APIRouter, Depends, status
from src.dependencies.rag import get_rag_service
from src.schemas.retrieval import UserInput
from src.services.rag import Rag
from fastapi.responses import StreamingResponse
import asyncio

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
)
async def retrieve_restaurants(
    input: UserInput,
    rag_service: Rag = Depends(get_rag_service),
):
  try:
    return StreamingResponse(
        rag_service.get_sse_response(
            question=input.user_input,
        ),
        media_type="text/event-stream",
    )
  except asyncio.TimeoutError:
    return StreamingResponse("event: responseUpdate\ndata: [Timeout reached.]")
