from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..services.ai_service import build_exam_prompt
from ..services.exam_service import generate_and_persist_exam
from ..schemas.exam import ExamRequest, ExamResponse
from ..db.database import get_db

router = APIRouter()


@router.post("/exams", response_model=ExamResponse)
async def generate_exam(request: ExamRequest, db: Session = Depends(get_db)):
    prompt = build_exam_prompt(request.prompt)
    if request.class_id is None:
        raise ValueError("class_id is required to persist exams")
    return await generate_and_persist_exam(db, prompt, request.class_id, request.title)
