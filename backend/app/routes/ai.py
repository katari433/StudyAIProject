from fastapi import APIRouter

from ai_service import (
    call_mcp_ai_service,
    build_flashcard_prompt,
    build_exam_prompt,
    parse_flashcards,
    parse_exam,
    FlashcardRequest,
    ExamRequest,
    FlashcardResponse,
    ExamResponse
)

router = APIRouter()


@router.post("/flashcards", response_model=FlashcardResponse)
async def generate_flashcards(request: FlashcardRequest):
    prompt = build_flashcard_prompt(request.prompt)
    ai_response = await call_mcp_ai_service(prompt)
    return parse_flashcards(ai_response)


@router.post("/exams", response_model=ExamResponse)
async def generate_exam(request: ExamRequest):
    prompt = build_exam_prompt(request.prompt)
    ai_response = await call_mcp_ai_service(prompt)
    return parse_exam(ai_response)
