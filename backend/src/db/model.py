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


class UserDB(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    password = Column(String(256))
    ms_oid = Column(String, default=None)
    is_active = Column(Boolean, default=True)

    notes = relationship("NoteDB", back_populates="user")
    note_access = relationship("NoteAccessDB", back_populates="user")


class NoteDB(Base):
    __tablename__ = "note"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    # owner
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("UserDB", back_populates="notes")

    note_access = relationship("NoteAccessDB", back_populates="note")
    tags = relationship("NoteTagDB", back_populates="note")


class NoteAccessDB(Base):
    __tablename__ = "note_access"

    note_id = Column(Integer, ForeignKey("note.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)

    note = relationship("NoteDB", back_populates="note_access")
    user = relationship("UserDB", back_populates="note_access")


class NoteTagDB(Base):
    __tablename__ = "note_tag"

    note_id = Column(Integer, ForeignKey("note.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tag.id"), primary_key=True)

    note = relationship("NoteDB", back_populates="tags")
    tag = relationship("TagDB", back_populates="notes")


class TagDB(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    notes = relationship("NoteTagDB", back_populates="tag")


Base.metadata.create_all(engine)
