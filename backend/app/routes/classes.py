# classes.py - charles cain
# class endpoints for API

# imports
from datetime import datetime

from fastapi import HTTPException
from fastapi import APIRouter

# TODO import schemas - may need to change later
from ..schemas.classes import ClassResponse, ClassCreate

# TODO may need to change databases later
classes_db: dict[int, ClassResponse] = {}
exams_db: dict[int, ClassResponse] = {}
flashcards_db: dict[int, ClassResponse] = {}

# create api router
router = APIRouter()


# POST - create_class adds a new class:
@router.post("/classes", response_model=ClassResponse)
async def create_class(class_data: ClassCreate):
    class_id = len(classes_db) + 1

    new_class = ClassResponse(
        id=class_id,
        name=class_data.name,
        description=class_data.description,
        created_at=datetime.now(),
    )

    classes_db[class_id] = new_class
    return new_class


# GET - gets all classes, returns a list object
@router.get("/classes", response_model=list[ClassResponse])
async def get_all_classes():
    return list(classes_db.values())


# GET - gets one class by class ID
@router.get("/classes/{class_id}", response_model=ClassResponse)
async def get_single_class(class_id: int):
    if class_id not in classes_db:
        raise HTTPException(status_code=404, detail="Class not found")

    return classes_db[class_id]


# DELETE - deletes a class by class ID - all materials in class should also be deleted,
#         including flashcards, exams that have been generated
@router.delete("/classes/{class_id}")
async def delete_class(class_id: int):
    if class_id not in classes_db:
        raise HTTPException(status_code=404, detail="Class not found")

    del classes_db[class_id]

    # deletes flashcards by class_id
    for flashcard_id in list(flashcards_db.keys()):
        if getattr(flashcards_db[flashcard_id], "class_id", None) == class_id:
            del flashcards_db[flashcard_id]

    # deletes exams by class_id
    for exam_id in list(exams_db.keys()):
        if getattr(exams_db[exam_id], "class_id", None) == class_id:
            del exams_db[exam_id]

    return {"message": "Class and related study materials deleted successfully"}
