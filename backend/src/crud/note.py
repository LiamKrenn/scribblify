from api.model.note import Note, NoteSchema
from db.session import session
from db.model import NoteDB

DATA_DIR = "/home/arch/code/school/ITP/scribblify/backend/data/"


def create_note(note: Note) -> NoteSchema:
    db_note = NoteDB(**note.model_dump())
    session.add(db_note)
    session.commit()

    with open(DATA_DIR + note.title, "w") as file:
        pass

    return NoteSchema(id=db_note.id, user_id=0, **note.model_dump())


def get_note_file(note_id: int):
    return open(DATA_DIR + str(note_id), "r")
