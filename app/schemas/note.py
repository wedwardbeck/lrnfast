from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class NoteSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=50)


class NoteDB(NoteSchema):
    id: int
    title: str
    description: str
    owner_id: int
    created_date: datetime
    changed_date: Optional[datetime] = None
    changed_by: Optional[int] = None


class NoteUser(NoteSchema):
    id: int
    title: str
    description: str
    created_date: datetime
    changed_date: Optional[datetime] = None
    owner: str
