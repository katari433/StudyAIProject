from fastapi import APIRouter

from ..services.ai_service import build_exam_prompt, call_mcp_ai_service, parse_exam
from ..schemas.exam import ExamRequest, ExamResponse

router = APIRouter()


@router.post("/exams", response_model=ExamResponse)
async def generate_exam(request: ExamRequest):
    prompt = build_exam_prompt(request.prompt)
    ai_response = await call_mcp_ai_service(prompt)
    return parse_exam(ai_response)
