from api.model.base import Base


class User(Base):
    password: str
    email: str


class UserSchema(User):
    ms_oid: str
    is_active: bool
    id: int
