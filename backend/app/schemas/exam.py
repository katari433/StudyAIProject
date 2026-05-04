from typing import List, Optional
from pydantic import BaseModel


class ExamRequest(BaseModel):
    prompt: str
    class_id: Optional[int] = None
    title: Optional[str] = "AI Generated Exam"


class ExamQuestion(BaseModel):
    question_type: str
    question: str
    choices: Optional[List[str]] = None
    correct_answer: str


class ExamResponse(BaseModel):
    questions: List[ExamQuestion]
