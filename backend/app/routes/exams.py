from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..services.ai_service import build_exam_prompt
from ..services.exam_service import generate_and_persist_exam
from ..schemas.exam import (
    ExamRequest,
    ExamResponse,
    ExamListResponse,
    ExamModelResponse,
)
from ..db.database import get_db

router = APIRouter()


@router.post("/exams", response_model=ExamResponse)
async def generate_exam(request: ExamRequest, db: Session = Depends(get_db)):
    prompt = build_exam_prompt(request.prompt)
    if request.class_id is None:
        raise ValueError("class_id is required to persist exams")
    return await generate_and_persist_exam(db, prompt, request.class_id, request.title)


@router.get("/exams", response_model=ExamListResponse)
def list_exams(class_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(__import__("app").db.models.Exam)
    if class_id is not None:
        query = query.filter(__import__("app").db.models.Exam.class_id == class_id)

    items = []
    for e in query.all():
        items.append(
            {
                "id": e.id,
                "title": e.title,
                "class_id": e.class_id,
                "questions": e.questions or [],
                "created_at": e.created_at,
            }
        )

    return {"exams": items}


@router.get("/exams/{exam_id}", response_model=ExamModelResponse)
def get_exam(exam_id: int, db: Session = Depends(get_db)):
    e = (
        db.query(__import__("app").db.models.Exam)
        .filter(__import__("app").db.models.Exam.id == exam_id)
        .first()
    )
    if not e:
        raise __import__("fastapi").HTTPException(
            status_code=404, detail="Exam not found"
        )

    return {
        "id": e.id,
        "title": e.title,
        "class_id": e.class_id,
        "questions": e.questions or [],
        "created_at": e.created_at,
    }
