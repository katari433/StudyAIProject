from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class FlashcardRequest(BaseModel):
    prompt: str
    class_id: Optional[int] = None
    set_title: Optional[str] = "AI Generated Set"


class Flashcard(BaseModel):
    question: str
    answer: str


class FlashcardResponse(BaseModel):
    flashcards: List[Flashcard]


class FlashcardSetResponse(BaseModel):
    id: int
    title: str
    class_id: int
    created_at: Optional[datetime] = None
    flashcards: List[Flashcard] = []


class FlashcardSetListResponse(BaseModel):
    sets: List[FlashcardSetResponse]
