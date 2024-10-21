from typing import List
from api.model.note import Note, NoteSchema
from api.model.page import Page
from api.model.user import UserSchema

from db.session import session
from db.model import NoteDB

from crud.utils.page import pageinate

import os

DATA_DIR = str(os.getcwd())


def create_note(note: Note, user: UserSchema) -> NoteSchema:
    db_note = NoteDB(**note.model_dump(), user_id=user.id)
    session.add(db_note)
    session.commit()

    return NoteSchema.model_validate(db_note)


def get_note_file(note_id: int):
    return open(DATA_DIR + str(note_id), "rw")


def delete_note(note_id: int):
    note = session.query(NoteDB).filter(NoteDB.id == note_id).first()
    session.delete(note)
    session.commit()


def get_notes(page: Page) -> list[NoteSchema]:
    db_notes: List[NoteDB] = pageinate(session.query(NoteDB), page).all()
    return [NoteSchema.model_validate(note) for note in db_notes]
