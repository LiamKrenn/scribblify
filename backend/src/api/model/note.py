from pydantic import BaseModel


class Note(BaseModel):
    title: str


class NoteSchema(Note):
    id: int
    user_id: int
