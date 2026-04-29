#classes schema file - charles cain

#imports
from typing import Optional
from pydantic import Field, BaseModel
from datetime import datetime

class ClassCreate(BaseModel):
    name: str = Field(..., example="Intro to Biology")
    description: Optional[str] = Field(None, example="Covers cells, genetics, and evolution.")

class ClassResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime