"""
Study Assistant REST API Skeleton

Project Goal:
-------------
This API stores study materials by class and uses AI to generate
study tools such as flashcards and practice exams.

Main Features Planned:
----------------------
- Class creation
- Get all classes
- Get single class
- Delete class with cascade handling
- Flashcard generation
- Get flashcard sets by class
- Get single flashcard set
- Delete flashcard set
- Practice exam generation
- Get exams by class
- Get single exam
- Delete exam
- AI response parsing and validation
- Environment variable configuration
- Database schema setup

Recommended command to run:
---------------------------
uvicorn main:app --reload
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import os


# ---------------------------------------------------------
# App Setup
# ---------------------------------------------------------

app = FastAPI(
    title="Study Assistant API",
    description="REST API for managing classes and generating AI-powered study materials.",
    version="0.1.0"
)


# ---------------------------------------------------------
# Environment Variables
# ---------------------------------------------------------

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///study_assistant.db")
AI_API_KEY = os.getenv("AI_API_KEY", "replace-with-real-key")


# ---------------------------------------------------------
# Temporary In-Memory Storage
# Replace this later with real database models.
# ---------------------------------------------------------

classes_db = {}
flashcards_db = {}
exams_db = {}


# ---------------------------------------------------------
# Pydantic Schemas
# ---------------------------------------------------------

class ClassCreate(BaseModel):
    name: str = Field(..., example="Intro to Biology")
    description: Optional[str] = Field(None, example="Covers cells, genetics, and evolution.")


class ClassResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime


class FlashcardGenerationRequest(BaseModel):
    class_id: int
    source_text: str = Field(..., example="Photosynthesis converts light energy into chemical energy.")


class Flashcard(BaseModel):
    question: str
    answer: str


class FlashcardSetResponse(BaseModel):
    id: int
    class_id: int
    flashcards: List[Flashcard]
    created_at: datetime


class ExamGenerationRequest(BaseModel):
    class_id: int
    source_text: str
    number_of_questions: int = Field(5, ge=1, le=50)


class ExamQuestion(BaseModel):
    question: str
    choices: List[str]
    correct_answer: str


class ExamResponse(BaseModel):
    id: int
    class_id: int
    questions: List[ExamQuestion]
    created_at: datetime


# ---------------------------------------------------------
# AI Service Skeleton
# ---------------------------------------------------------

def call_ai_service(prompt: str) -> str:
    """
    Sends a prompt to the AI service.

    Replace this function with your actual AI/MCP/OpenAI/Open Claw integration.
    """
    return "AI response placeholder"


def build_flashcard_prompt(source_text: str) -> str:
    """
    Builds a prompt for flashcard generation.
    """
    return f"""
    Create flashcards from the following study material.
    Return the response in JSON format.

    Study Material:
    {source_text}
    """


def build_exam_prompt(source_text: str, number_of_questions: int) -> str:
    """
    Builds a prompt for practice exam generation.
    """
    return f"""
    Create a practice exam with {number_of_questions} questions.
    Return the response in JSON format.

    Study Material:
    {source_text}
    """


def parse_flashcard_response(ai_response: str) -> List[Flashcard]:
    """
    Parses and validates the AI flashcard response.

    This is currently hardcoded.
    Later, replace this with JSON parsing and validation.
    """
    return [
        Flashcard(
            question="Sample question?",
            answer="Sample answer."
        )
    ]


def parse_exam_response(ai_response: str) -> List[ExamQuestion]:
    """
    Parses and validates the AI exam response.

    This is currently hardcoded.
    Later, replace this with JSON parsing and validation.
    """
    return [
        ExamQuestion(
            question="Sample multiple choice question?",
            choices=["A", "B", "C", "D"],
            correct_answer="A"
        )
    ]


# ---------------------------------------------------------
# Class Endpoints
# ---------------------------------------------------------

@app.post("/classes", response_model=ClassResponse)
def create_class(class_data: ClassCreate):
    """
    Create a new class.
    """
    class_id = len(classes_db) + 1

    new_class = ClassResponse(
        id=class_id,
        name=class_data.name,
        description=class_data.description,
        created_at=datetime.now()
    )

    classes_db[class_id] = new_class
    return new_class


@app.get("/classes", response_model=List[ClassResponse])
def get_all_classes():
    """
    Get all saved classes.
    """
    return list(classes_db.values())


@app.get("/classes/{class_id}", response_model=ClassResponse)
def get_single_class(class_id: int):
    """
    Get one class by ID.
    """
    if class_id not in classes_db:
        raise HTTPException(status_code=404, detail="Class not found")

    return classes_db[class_id]


@app.delete("/classes/{class_id}")
def delete_class(class_id: int):
    """
    Delete a class.

    Later, this should also delete related flashcard sets and exams
    from the database using cascade handling.
    """
    if class_id not in classes_db:
        raise HTTPException(status_code=404, detail="Class not found")

    del classes_db[class_id]

    # Simple cascade handling for temporary storage
    for flashcard_id in list(flashcards_db.keys()):
        if flashcards_db[flashcard_id].class_id == class_id:
            del flashcards_db[flashcard_id]

    for exam_id in list(exams_db.keys()):
        if exams_db[exam_id].class_id == class_id:
            del exams_db[exam_id]

    return {"message": "Class and related study materials deleted successfully"}


# ---------------------------------------------------------
# Flashcard Endpoints
# ---------------------------------------------------------

@app.post("/flashcards/generate", response_model=FlashcardSetResponse)
def generate_flashcards(request: FlashcardGenerationRequest):
    """
    Generate a flashcard set for a class using AI.
    """
    if request.class_id not in classes_db:
        raise HTTPException(status_code=404, detail="Class not found")

    prompt = build_flashcard_prompt(request.source_text)
    ai_response = call_ai_service(prompt)
    flashcards = parse_flashcard_response(ai_response)

    flashcard_set_id = len(flashcards_db) + 1

    new_set = FlashcardSetResponse(
        id=flashcard_set_id,
        class_id=request.class_id,
        flashcards=flashcards,
        created_at=datetime.now()
    )

    flashcards_db[flashcard_set_id] = new_set
    return new_set


@app.get("/classes/{class_id}/flashcards", response_model=List[FlashcardSetResponse])
def get_flashcards_by_class(class_id: int):
    """
    Get all flashcard sets for a specific class.
    """
    if class_id not in classes_db:
        raise HTTPException(status_code=404, detail="Class not found")

    return [
        flashcard_set
        for flashcard_set in flashcards_db.values()
        if flashcard_set.class_id == class_id
    ]


@app.get("/flashcards/{flashcard_set_id}", response_model=FlashcardSetResponse)
def get_single_flashcard_set(flashcard_set_id: int):
    """
    Get one flashcard set by ID.
    """
    if flashcard_set_id not in flashcards_db:
        raise HTTPException(status_code=404, detail="Flashcard set not found")

    return flashcards_db[flashcard_set_id]


@app.delete("/flashcards/{flashcard_set_id}")
def delete_flashcard_set(flashcard_set_id: int):
    """
    Delete a flashcard set.
    """
    if flashcard_set_id not in flashcards_db:
        raise HTTPException(status_code=404, detail="Flashcard set not found")

    del flashcards_db[flashcard_set_id]
    return {"message": "Flashcard set deleted successfully"}


# ---------------------------------------------------------
# Practice Exam Endpoints
# ---------------------------------------------------------

@app.post("/exams/generate", response_model=ExamResponse)
def generate_practice_exam(request: ExamGenerationRequest):
    """
    Generate a practice exam for a class using AI.
    """
    if request.class_id not in classes_db:
        raise HTTPException(status_code=404, detail="Class not found")

    prompt = build_exam_prompt(request.source_text, request.number_of_questions)
    ai_response = call_ai_service(prompt)
    questions = parse_exam_response(ai_response)

    exam_id = len(exams_db) + 1

    new_exam = ExamResponse(
        id=exam_id,
        class_id=request.class_id,
        questions=questions,
        created_at=datetime.now()
    )

    exams_db[exam_id] = new_exam
    return new_exam


@app.get("/classes/{class_id}/exams", response_model=List[ExamResponse])
def get_exams_by_class(class_id: int):
    """
    Get all practice exams for a specific class.
    """
    if class_id not in classes_db:
        raise HTTPException(status_code=404, detail="Class not found")

    return [
        exam
        for exam in exams_db.values()
        if exam.class_id == class_id
    ]


@app.get("/exams/{exam_id}", response_model=ExamResponse)
def get_single_exam(exam_id: int):
    """
    Get one practice exam by ID.
    """
    if exam_id not in exams_db:
        raise HTTPException(status_code=404, detail="Exam not found")

    return exams_db[exam_id]


@app.delete("/exams/{exam_id}")
def delete_exam(exam_id: int):
    """
    Delete a practice exam.
    """
    if exam_id not in exams_db:
        raise HTTPException(status_code=404, detail="Exam not found")

    del exams_db[exam_id]
    return {"message": "Exam deleted successfully"}


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@app.get("/")
def root():
    """
    Basic API health check.
    """
    return {
        "message": "Study Assistant API is running",
        "version": "0.1.0"
    }
