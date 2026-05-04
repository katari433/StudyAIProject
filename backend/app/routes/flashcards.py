from fastapi import APIRouter

from ..services.ai_service import (
    build_flashcard_prompt,
    call_mcp_ai_service,
    parse_flashcards,
)
from ..schemas.flashcard import FlashcardRequest, FlashcardResponse

router = APIRouter()


@router.post("/flashcards", response_model=FlashcardResponse)
async def generate_flashcards(request: FlashcardRequest):
    prompt = build_flashcard_prompt(request.prompt)
    ai_response = await call_mcp_ai_service(prompt)
    return parse_flashcards(ai_response)
