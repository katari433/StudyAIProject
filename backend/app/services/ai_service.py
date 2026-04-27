import json
from typing import List, Optional

from fastapi import HTTPException
from pydantic import BaseModel

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client



# SCHEMAS


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



# MCP CALL


async def call_mcp_ai_service(prompt: str) -> str:
    server_params = StdioServerParameters(
        command="python3",
        args=["mcp_study_server.py"],
    )

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                response = await session.call_tool(
                    "generate",
                    {"prompt": prompt}
                )
                return response.content

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# PROMPT BUILDERS


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
"""



# PARSING


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
