from typing import List

from api.model.note_access import NoteAccess
from api.model.user import UserPublic

from db.model import NoteAccessDB, UserDB
from db.session import session


def add_note_access(note_access: NoteAccess):
    db = NoteAccessDB(**note_access.model_dump())
    session.add(db)
    session.commit()


def get_note_access(note_id: int, user: UserPublic) -> List[UserPublic]:
    db = (
        session.query(NoteAccessDB)
        .join(UserDB)
        .filter(NoteAccessDB.note_id == note_id)
        .filter(UserDB.id == user.id)
        .all()
    )
    return [UserPublic.model_validate(note) for note in db]


def delete_note_access(note_id: int, user_id: int):
    db = (
        session.query(NoteAccessDB)
        .filter(NoteAccessDB.note_id == note_id)
        .filter(NoteAccessDB.user_id == user_id)
        .first()
    )
    session.delete(db)
    session.commit()
