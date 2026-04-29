from fastapi import FastAPI
from .routes.ai import router as ai_router

app = FastAPI(
    title="Study AI API",
    description="FastAPI app to generate flashcards and practice exams.",
    version="0.1.0"
)

@app.get("/")
def root():
    return {"message": "Study AI API is running"}

# This line connects the modular routes to the app
app.include_router(ai_router)