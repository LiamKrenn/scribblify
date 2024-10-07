from datetime import datetime
from typing import List
from sqlalchemy import (
    Column,
    Integer,
    String,
    Double,
    Boolean,
    ForeignKey,
    DateTime,
    Table,
)
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

from db.session import engine, session

Base = declarative_base()


class NoteDB(Base):
    __tablename__ = "note"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    # owner
    user_id = Column(Integer, default=0)


class NoteAccessDB(Base):
    __tablename__ = "note_access"

    note_id = Column(Integer, ForeignKey("note.id"), primary_key=True)
    user_id = Column(Integer, primary_key=True)

    note = relationship("NoteDB", back_populates="note_access")


Base.metadata.create_all(engine)
