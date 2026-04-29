"""
Database Configuration and Session Management

This module provides centralized database setup for the StudyAI backend using SQLAlchemy ORM.
It handles:
- Engine initialization from DATABASE_URL environment variable
- Session factory creation with proper configuration
- Declarative base for ORM model definitions
- FastAPI dependency injection for database sessions

Environment Variables:
    DATABASE_URL: Connection string for the database. Defaults to SQLite for development.
                  Format: postgresql://user:password@localhost/dbname for PostgreSQL
                  Format: sqlite:///./studyai.db for SQLite (default)

Usage in FastAPI:
    from fastapi import Depends
    from sqlalchemy.orm import Session
    from .database import get_db

    @app.get("/items/")
    def read_items(db: Session = Depends(get_db)):
        items = db.query(Item).all()
        return items

Migrations:
    This module is integrated with Alembic for schema versioning and migrations.
    Run migrations with: alembic upgrade head
"""

from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator

# Load environment variables from .env file
_HERE = os.path.dirname(__file__)
load_dotenv(os.path.join(_HERE, "..", "..", ".env"))

# Database connection URL from environment or default to SQLite
# For production, use PostgreSQL: DATABASE_URL=postgresql://user:pass@host/db
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./studyai.db")

# SQLite requires special handling; PostgreSQL does not
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    # SQLite: allow concurrent access from different threads in test environment
    connect_args["check_same_thread"] = False

# Create database engine
# echo=False for production; set echo=True for debugging SQL queries
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    # For PostgreSQL connection pooling, uncomment: pool_pre_ping=True, pool_size=10, max_overflow=20
)

# Session factory for creating new database sessions
# autocommit=False: transactions must be explicitly committed
# autoflush=False: objects are not flushed to database until explicitly committed
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base class for all ORM models
# All model classes in models.py should inherit from this Base
Base = declarative_base()


def get_db() -> Generator:
    """
    FastAPI dependency that provides a database session for each request.

    Usage:
        @app.get("/users/")
        def list_users(db: Session = Depends(get_db)):
            return db.query(User).all()

    Yields:
        Session: SQLAlchemy database session

    Ensures:
        - Session is properly closed after request completes
        - Session is closed even if an exception occurs (via finally block)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
