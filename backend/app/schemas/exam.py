from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


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


class ExamModelResponse(BaseModel):
    id: int
    title: str
    class_id: int
    questions: List[dict]
    created_at: Optional[datetime] = None


class ExamListResponse(BaseModel):
    exams: List[ExamModelResponse]
