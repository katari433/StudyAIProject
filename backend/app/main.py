from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    """Application factory for the StudyAI FastAPI app.

    Returns a configured FastAPI application instance with routers registered.
    """
    from .routes.ai import router as ai_router
    from .routes.classes import router as classes_router

    app = FastAPI(
        title="Study AI API",
        description="FastAPI app using MCP to generate flashcards and practice exams.",
        version="0.1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    def root():
        return {"message": "Study AI API is running with MCP"}

    # Register routes
    app.include_router(ai_router)
    app.include_router(classes_router)

    return app


# Module-level app instance used by ASGI servers
app = create_app()
