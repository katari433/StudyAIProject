from pydantic import BaseModel, Field
from typing import List, Optional
import json
import openai 

# ---------------------------------------------------------
# Pydantic Schemas
# ---------------------------------------------------------

# Exam Schemas
class ExamRequest(BaseModel):
    prompt: str  # The study material/notes
    number_of_questions: int = 5 

class ExamQuestion(BaseModel):
    question: str
    choices: List[str]
    correct_answer: str

class ExamResponse(BaseModel):
    questions: List[ExamQuestion]

# Flashcard Schemas (Skeletons)
class FlashcardRequest(BaseModel):
    prompt: str

class Flashcard(BaseModel):
    question: str
    answer: str

class FlashcardResponse(BaseModel):
    flashcards: List[Flashcard]


# ---------------------------------------------------------
# AI Service / MCP Integration
# ---------------------------------------------------------

async def call_mcp_ai_service(prompt: str) -> str:
    """
    Connects to the OpenAI API via MCP. 
    Currently returns a mock JSON string for testing logic flow.
    """
    # TODO: Integrate real OpenAI AsyncOpenAI client here
    # Example Mock Response:
    mock_response = {
        "questions": [
            {
                "question": "What is the primary goal of this AI project?",
                "choices": ["To play games", "To generate study tools", "To cook food", "To browse social media"],
                "correct_answer": "To generate study tools"
            }
        ]
    }
    return json.dumps(mock_response)


# ---------------------------------------------------------
# Prompt Builders (Issue #13 & #14)
# ---------------------------------------------------------

def build_exam_prompt(source_text: str, num_questions: int = 5) -> str:
    """
    Issue #14: Creates a structured prompt for multiple-choice exams.
    """
    return f"""
    Create a {num_questions}-question multiple-choice practice exam based on the following text.
    Return the response in a strict JSON format with a "questions" key.
    Each question must have exactly 4 choices and 1 correct_answer string.

    TEXT:
    {source_text}
    """

def build_flashcard_prompt(source_text: str) -> str:
    """
    Issue #13: Skeleton for flashcard prompt generation.
    """
    return f"Generate a JSON list of flashcards for the following material: {source_text}"


# ---------------------------------------------------------
# Response Parsers (Issue #15 & #16)
# ---------------------------------------------------------

def parse_exam(ai_response: str) -> ExamResponse:
    """
    Issue #15: Validates AI response and converts it into an ExamResponse object.
    """
    try:
        # Clean up possible markdown formatting (e.g., ```json ... ```)
        clean_json = ai_response.strip().replace("```json", "").replace("```", "")
        data = json.loads(clean_json)
        
        # This maps the raw dictionary to our Pydantic classes
        return ExamResponse(questions=[ExamQuestion(**q) for q in data["questions"]])
    except Exception as e:
        print(f"Parsing error in Exam: {e}")
        return ExamResponse(questions=[])

def parse_flashcards(ai_response: str) -> FlashcardResponse:
    """
    Skeleton for flashcard response parsing.
    """
    # Temporary mock return to prevent errors
    return FlashcardResponse(flashcards=[Flashcard(question="Mock?", answer="Mock.")])