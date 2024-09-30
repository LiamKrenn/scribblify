from api.model.note import Note, NoteSchema
from api.model.page import Page

from db.session import session
from db.model import NoteDB

from crud.utils.page import pageinate

import os

DATA_DIR = str(os.getcwd())


def create_note(note: Note) -> NoteSchema:
    db_note = NoteDB(**note.model_dump())
    session.add(db_note)
    session.commit()

    return NoteSchema(id=db_note.id, user_id=0, **note.model_dump())


def get_note_file(note_id: int):
    return open(DATA_DIR + str(note_id), "rw")


def get_notes(page: Page) -> list[NoteSchema]:
    db_notes = pageinate(session.query(NoteDB), page).all()
    return [NoteSchema(id=note.id, user_id=0, title=note.title) for note in db_notes]
