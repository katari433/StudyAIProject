from fastapi import FastAPI
from routes import router as ai_router

app = FastAPI(
    title="Study AI API",
    description="FastAPI app using MCP to generate flashcards and practice exams.",
    version="0.1.0"
)

@app.get("/")
def root():
    return {"message": "Study AI API is running with MCP"}

# Register routes
app.include_router(ai_router)
