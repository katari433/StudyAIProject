from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..services.ai_service import build_flashcard_prompt
from ..services.flashcard_service import generate_and_persist_flashcards
from ..schemas.flashcard import FlashcardRequest, FlashcardResponse
from ..db.database import get_db

router = APIRouter()


@router.post("/flashcards", response_model=FlashcardResponse)
async def generate_flashcards(request: FlashcardRequest, db: Session = Depends(get_db)):
    prompt = build_flashcard_prompt(request.prompt)
    if request.class_id is None:
        raise ValueError("class_id is required to persist flashcards")
    return await generate_and_persist_flashcards(
        db, prompt, request.class_id, request.set_title
    )
