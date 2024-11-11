from typing import List
from api.model.user import User, UserSchema

from db.session import session
from db.model import UserDB

import crud
from crud import utils

from crud.utils.hash import hash
from crud.utils.page import pageinate


def create_user(user: User) -> UserSchema:
    user.password = hash(user.password)
    db_user = UserDB(**user.model_dump())
    session.add(db_user)
    session.commit()

    return db_user.id


def authenticate_user(email: str, password: str) -> UserSchema:
    password = hash(password)
    user: UserDB = session.query(UserDB).filter(UserDB.email == email).first()

    if user is None:
        return None

    if user.password != password:
        return None

    return UserSchema.model_validate(user)


def get_user(email: str) -> UserSchema:
    user: UserDB = session.query(UserDB).filter(UserDB.email == email).first()

    if user is None:
        return None

    return UserSchema.model_validate(user)


def get_user_ms(oid: str) -> UserSchema:
    user: UserDB = session.query(UserDB).filter(UserDB.ms_oid == oid).first()

    if user is None:
        return None

    return UserSchema.model_validate(user)


def login_ms(oid: str) -> UserSchema:
    user: UserDB = session.query(UserDB).filter(UserDB.ms_oid == oid).first()

    if user is None:
        return None

    return UserSchema.model_validate(user)


def create_user_ms(user: User, oid: str) -> UserSchema:
    db_user = UserDB(**user.model_dump(), ms_oid=oid)
    session.add(db_user)
    session.commit()

    return UserSchema.model_validate(db_user)


def get_users(page: dict) -> List[UserSchema]:
    users = pageinate(session.query(UserDB), page).all()
    return [UserSchema.model_validate(user) for user in users]
