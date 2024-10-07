from api.model.base import Base


class NoteAccess(Base):
    note_id: int
    user_id: int
