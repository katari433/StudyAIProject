from typing import Any
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db import models

from .ai_service import call_mcp_ai_service, parse_exam
from ..schemas.exam import ExamResponse
from fastapi.concurrency import run_in_threadpool


async def generate_and_persist_exam(
    db: Session, prompt: str, class_id: int, title: str = "AI Generated Exam"
) -> ExamResponse:
    """Generate an exam via AI and persist it under the given class_id.

    Returns the parsed `ExamResponse`.
    """
    ai_text = await call_mcp_ai_service(prompt)
    parsed: ExamResponse = parse_exam(ai_text)

    def _persist():
        klass = db.query(models.Class).filter(models.Class.id == class_id).first()
        if not klass:
            raise HTTPException(status_code=404, detail="Class not found")

        exam = models.Exam(
            title=title,
            class_id=class_id,
            questions=[q.dict() for q in parsed.questions],
        )
        db.add(exam)
        db.commit()
        db.refresh(exam)
        return exam

    await run_in_threadpool(_persist)
    return parsed


def build_exam_prompt(source_text: str, number_of_questions: int) -> str:
    """
    Constructs the system and user instructions for OpenAI.
    """
    return f"""
    You are an expert academic assistant. Create a practice exam based on the provided text.
    
    STRICT RULES:
    1. Generate exactly {number_of_questions} multiple-choice questions.
    2. Each question must have exactly 4 choices (A, B, C, D).
    3. Return ONLY a JSON object with a key "questions" containing a list of objects.
    4. Each question object must have: "question", "choices", and "correct_answer".
    
    SOURCE TEXT:
    {source_text}
    """
