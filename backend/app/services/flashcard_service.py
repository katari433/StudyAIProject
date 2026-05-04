from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db import models

from .ai_service import call_mcp_ai_service, parse_flashcards
from ..schemas.flashcard import FlashcardResponse
from fastapi.concurrency import run_in_threadpool


async def generate_and_persist_flashcards(
    db: Session, prompt: str, class_id: int, set_title: str = "AI Generated Set"
) -> FlashcardResponse:
    """Generate flashcards via AI service and persist them into DB under given class_id.

    Returns the parsed `FlashcardResponse`.
    """
    ai_text = await call_mcp_ai_service(prompt)
    parsed: FlashcardResponse = parse_flashcards(ai_text)

    def _persist():
        # verify class exists
        klass = db.query(models.Class).filter(models.Class.id == class_id).first()
        if not klass:
            raise HTTPException(status_code=404, detail="Class not found")

        flashcard_set = models.FlashcardSet(title=set_title, class_id=class_id)
        db.add(flashcard_set)
        db.flush()  # assign id

        for fc in parsed.flashcards:
            card = models.Flashcard(
                question=fc.question, answer=fc.answer, set_id=flashcard_set.id
            )
            db.add(card)

        db.commit()
        db.refresh(flashcard_set)
        return flashcard_set

    # Run DB persistence in threadpool
    await run_in_threadpool(_persist)
    return parsed
