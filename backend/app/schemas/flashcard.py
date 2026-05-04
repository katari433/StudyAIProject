from typing import List, Optional
from pydantic import BaseModel


class FlashcardRequest(BaseModel):
    prompt: str
    class_id: Optional[int] = None
    set_title: Optional[str] = "AI Generated Set"


class Flashcard(BaseModel):
    question: str
    answer: str


class FlashcardResponse(BaseModel):
    flashcards: List[Flashcard]
