import json
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ai_service import call_mcp_ai_service

app = FastAPI(
    title="Study AI API",
    description="FastAPI app using MCP to generate flashcards and practice exams.",
    version="0.1.0"
)



# Pydantic Schemas


class FlashcardRequest(BaseModel):
    prompt: str


class ExamRequest(BaseModel):
    prompt: str


class Flashcard(BaseModel):
    question: str
    answer: str


class FlashcardResponse(BaseModel):
    flashcards: List[Flashcard]


class ExamQuestion(BaseModel):
    question_type: str
    question: str
    choices: Optional[List[str]] = None
    correct_answer: str


class ExamResponse(BaseModel):
    questions: List[ExamQuestion]


# Prompt Builders


def build_flashcard_prompt(user_prompt: str) -> str:
    return f"""
Create flashcards based on this user request:

{user_prompt}

Return ONLY raw valid JSON in this exact format:

{{
  "flashcards": [
    {{
      "question": "question text",
      "answer": "answer text"
    }}
  ]
}}

Rules:
- Follow the user's requested topic and number of flashcards.
- Each flashcard must have a question and answer.
- Do not include markdown.
- Do not include explanations outside the JSON.
"""


def build_exam_prompt(user_prompt: str) -> str:
    return f"""
Create a practice exam based on this user request:

{user_prompt}

Return ONLY raw valid JSON in this exact format:

{{
  "questions": [
    {{
      "question_type": "true_false",
      "question": "question text",
      "choices": ["True", "False"],
      "correct_answer": "True"
    }},
    {{
      "question_type": "short_answer",
      "question": "question text",
      "choices": null,
      "correct_answer": "answer key text"
    }}
  ]
}}

Rules:
- Follow the user's requested topic, difficulty, and number of questions.
- Include true/false and short answer questions.
- Every question must include an answer key.
- The app does not grade answers; it only shows the answer key.
- Do not include markdown.
- Do not include explanations outside the JSON.
"""



#Parsers


def clean_json_response(ai_response: str) -> str:
    cleaned = ai_response.strip()

    if cleaned.startswith("```json"):
        cleaned = cleaned.replace("```json", "", 1).strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.replace("```", "", 1).strip()

    if cleaned.endswith("```"):
        cleaned = cleaned[:-3].strip()

    return cleaned


def parse_flashcards(ai_response: str) -> FlashcardResponse:
    try:
        cleaned = clean_json_response(ai_response)
        data = json.loads(cleaned)
        return FlashcardResponse(**data)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse flashcard response: {str(e)}"
        )


def parse_exam(ai_response: str) -> ExamResponse:
    try:
        cleaned = clean_json_response(ai_response)
        data = json.loads(cleaned)
        return ExamResponse(**data)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse exam response: {str(e)}"
        )

