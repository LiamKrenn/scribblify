from api.model.user import User, UserSchema

from db.session import session
from db.model import UserDB

import crud
from crud import utils

from crud.utils.hash import hash


def create_user(user: User) -> UserSchema:
    user.password = hash(user.password)
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
