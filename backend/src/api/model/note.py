from typing import Optional
from api.model.base import Base
from datetime import datetime


class Note(Base):
    title: str


class NoteSchema(Note):
    id: int
    user_id: Optional[int] = 0
    created_at: datetime
    updated_at: datetime
