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