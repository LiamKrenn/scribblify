from typing import List
from api.model.note import Note, NoteSchema
from api.model.page import Page
from api.model.user import UserSchema

from db.session import session
from db.model import NoteDB

from crud.utils.page import pageinate
from crud.utils.exceptions import UnauthorizedException
from crud.utils.rollback import crud_exception_handle

import os

DATA_DIR = str(os.getcwd())


@crud_exception_handle
def create_note(note: Note, user: UserSchema) -> NoteSchema:
    db_note = NoteDB(**note.model_dump(), user_id=user.id)
    session.add(db_note)
    session.commit()

    return NoteSchema.model_validate(db_note)


@crud_exception_handle
def get_note_file(note_id: int):
    try:
        return open(DATA_DIR + str(note_id), "r+")
    except FileNotFoundError:
        return open(DATA_DIR + str(note_id), "w+")


@crud_exception_handle
def get_note_content(note_id: int, user: UserSchema) -> str:
    note = (
        session.query(NoteDB)
        .filter(NoteDB.id == note_id)
        .filter(NoteDB.user_id == user.id)
        .first()
    )
    if note is None:
        raise UnauthorizedException(f"No access to note '{note_id}'")

    with open(DATA_DIR + str(note_id), "r+") as file:
        file.seek(0)
        return file.read()


@crud_exception_handle
def delete_note(note_id: int):
    note = session.query(NoteDB).filter(NoteDB.id == note_id).first()
    session.delete(note)
    session.commit()


@crud_exception_handle
def get_notes(page: Page, user: UserSchema) -> list[NoteSchema]:
    db_notes: List[NoteDB] = pageinate(
        session.query(NoteDB).filter(NoteDB.user_id == user.id), page
    ).all()
    return [NoteSchema.model_validate(note) for note in db_notes]
