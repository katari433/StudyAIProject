import json
import os
from typing import List, Optional

from fastapi import HTTPException

from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.client.session import ClientSession

from ..schemas.flashcard import FlashcardResponse
from ..schemas.exam import ExamResponse


async def call_mcp_ai_service(prompt: str) -> str:
    server_script = os.path.join(os.path.dirname(__file__), "..", "mcp_study_server.py")
    server_params = StdioServerParameters(
        command="python3",
        args=[os.path.abspath(server_script)],
    )

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                response = await session.call_tool(
                    "generate_study_material", arguments={"prompt": prompt}
                )

                if response.content and len(response.content) > 0:
                    first_item = response.content[0]
                    text_payload = getattr(first_item, "text", None)
                    if isinstance(text_payload, str) and text_payload.strip():
                        return text_payload
                    raise HTTPException(
                        status_code=500,
                        detail="MCP server returned unsupported content type",
                    )

                raise HTTPException(
                    status_code=500, detail="MCP server returned no content"
                )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"MCP AI service error: {str(e)}")


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
            status_code=500, detail=f"Failed to parse flashcard response: {str(e)}"
        )


def parse_exam(ai_response: str) -> ExamResponse:
    try:
        cleaned = clean_json_response(ai_response)
        data = json.loads(cleaned)
        return ExamResponse(**data)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to parse exam response: {str(e)}"
        )
