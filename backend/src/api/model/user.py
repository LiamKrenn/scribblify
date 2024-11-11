from typing import Optional
from api.model.base import Base


class User(Base):
    email: str


class UserPost(Base):
    password: Optional[str] = None
    email: str


class UserPublic(User):
    id: int


class UserSchema(User):
    ms_oid: str | None
    is_active: bool
    id: int
