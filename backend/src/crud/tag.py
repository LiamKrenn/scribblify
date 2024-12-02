from crud.utils.rollback import crud_exception_handle
from db.model import NoteDB, NoteTagDB, TagDB
from db.session import session

from api.model.tag import Tag, TagSchema


@crud_exception_handle
def add_tag(tag: Tag) -> TagSchema:
    db = TagDB(**tag.model_dump())
    session.add(db)
    session.commit()
    return TagSchema.model_validate(db)


@crud_exception_handle
def delete_tag(tag_id: int):
    db = session.query(TagDB).filter(TagDB.id == tag_id).first()
    session.delete(db)
    session.commit()
