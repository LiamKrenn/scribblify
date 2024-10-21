from api.model.user import User, UserSchema

from db.session import session
from db.model import UserDB

import crud
from crud import utils


def create_user(user: User) -> UserSchema:
    db_user = UserDB(**user.model_dump())
    session.add(db_user)
    session.commit()

    return db_user.id


def authenticate_user(email: str, password: str) -> UserSchema:
    password = hash(password)
    user = session.query(UserDB).filter(UserDB.email == email).first()

    if user.password != password:
        return None

    return UserSchema.model_validate(user)
