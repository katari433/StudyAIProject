"""
SQLAlchemy ORM Models for StudyAI Backend

This module defines the core data models for the StudyAI platform:
- User: Platform users with authentication credentials
- Class: Study classes owned by users, containing flashcard sets and exams
- FlashcardSet: Collections of flashcards organized by topic within a class
- Flashcard: Individual question-answer pairs within a flashcard set
- Exam: Generated assessments containing questions within a class

Relationships & Cascading:
- User → Class: One user owns many classes (cascade delete not set, allows shared classes)
- Class → FlashcardSet, Exam: One class has many sets and exams (cascade delete enabled)
- FlashcardSet → Flashcard: One set has many flashcards (cascade delete enabled)

Usage:
    from .models import User, Class, FlashcardSet
    from .database import SessionLocal
    
    db = SessionLocal()
    user = db.query(User).filter(User.email == "user@example.com").first()
    classes = user.classes  # Lazy-loaded relationship

Migrations:
    All models inherit from Base (defined in database.py).
    Alembic auto-generates migrations: alembic revision --autogenerate -m "Add new model"
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class User(Base):
    """User account model for StudyAI platform"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    classes = relationship("Class", back_populates="owner")


class Class(Base):
    """Study class model representing a course or topic"""
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="classes")
    flashcard_sets = relationship(
        "FlashcardSet",
        back_populates="klass",
        cascade="all, delete-orphan",
    )
    exams = relationship(
        "Exam",
        back_populates="klass",
        cascade="all, delete-orphan",
    )


class FlashcardSet(Base):
    """Flashcard set: collection of Q&A pairs on a specific topic"""
    __tablename__ = "flashcard_sets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    meta_info = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    klass = relationship("Class", back_populates="flashcard_sets")
    flashcards = relationship(
        "Flashcard",
        back_populates="flashcard_set",
        cascade="all, delete-orphan",
    )


class Flashcard(Base):
    """Flashcard model: single question-answer pair for studying"""
    __tablename__ = "flashcards"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    set_id = Column(Integer, ForeignKey("flashcard_sets.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    flashcard_set = relationship("FlashcardSet", back_populates="flashcards")


class Exam(Base):
    """Exam model: assessment with multiple questions from class material"""
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    questions = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    klass = relationship("Class", back_populates="exams")
