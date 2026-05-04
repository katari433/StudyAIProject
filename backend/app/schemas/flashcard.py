from typing import List
from pydantic import BaseModel


class FlashcardRequest(BaseModel):
    prompt: str


class Flashcard(BaseModel):
    question: str
    answer: str


class FlashcardResponse(BaseModel):
    flashcards: List[Flashcard]
