from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..services.ai_service import build_flashcard_prompt
from ..services.flashcard_service import generate_and_persist_flashcards
from ..schemas.flashcard import FlashcardRequest, FlashcardResponse
from ..schemas.flashcard import FlashcardSetResponse, FlashcardSetListResponse
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


@router.get("/sets", response_model=FlashcardSetListResponse)
def list_sets(class_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(__import__("app").db.models.FlashcardSet)
    if class_id is not None:
        query = query.filter(
            __import__("app").db.models.FlashcardSet.class_id == class_id
        )

    sets = []
    for s in query.all():
        flashcards = [
            {"question": f.question, "answer": f.answer} for f in s.flashcards
        ]
        sets.append(
            {
                "id": s.id,
                "title": s.title,
                "class_id": s.class_id,
                "created_at": s.created_at,
                "flashcards": flashcards,
            }
        )

    return {"sets": sets}


@router.get("/sets/{set_id}", response_model=FlashcardSetResponse)
def get_set(set_id: int, db: Session = Depends(get_db)):
    s = (
        db.query(__import__("app").db.models.FlashcardSet)
        .filter(__import__("app").db.models.FlashcardSet.id == set_id)
        .first()
    )
    if not s:
        raise __import__("fastapi").HTTPException(
            status_code=404, detail="Set not found"
        )

    flashcards = [{"question": f.question, "answer": f.answer} for f in s.flashcards]
    return {
        "id": s.id,
        "title": s.title,
        "class_id": s.class_id,
        "created_at": s.created_at,
        "flashcards": flashcards,
    }
