from typing import List
from api.model.note_access import NoteAccess

from db.model import NoteAccessDB
from db.session import session


def add_note_access(note_access: NoteAccess):
    db = NoteAccessDB(**note_access.model_dump())
    session.add(db)
    session.commit()


def get_note_access(note_id: int) -> List[NoteAccess]:
    db = session.query(NoteAccessDB).filter(NoteAccessDB.note_id == note_id).all()
    return [NoteAccess.model_validate(note) for note in db]


def delete_note_access(note_id: int, user_id: int):
    db = (
        session.query(NoteAccessDB)
        .filter(NoteAccessDB.note_id == note_id)
        .filter(NoteAccessDB.user_id == user_id)
        .first()
    )
    session.delete(db)
    session.commit()
