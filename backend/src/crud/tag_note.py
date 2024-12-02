from crud.utils.rollback import crud_exception_handle
from db.model import NoteDB, NoteTagDB, TagDB
from db.session import session

from api.model.tag import Tag, TagSchema


@crud_exception_handle
def add_note_tag(tag_id: int, note_id: int):
    notedb = session.query(NoteDB).filter(NoteDB.id == note_id).first()
    if notedb is None:
        raise ValueError(f"Note with id: '{note_id}' not found")

    tagdb = session.query(TagDB).filter(TagDB.id == tag_id).first()
    if tagdb is None:
        raise ValueError(f"Tag with id: '{tag_id}' not found")

    note_tag = NoteTagDB(note_id=note_id, tag_id=tag_id)
    session.add(note_tag)
    session.commit()


@crud_exception_handle
def delete_note_tag(tag_id: int, note_id: int):
    note_tag = (
        session.query(NoteTagDB)
        .filter(NoteTagDB.note_id == note_id, NoteTagDB.tag_id == tag_id)
        .first()
    )
    session.delete(note_tag)
    session.commit()
