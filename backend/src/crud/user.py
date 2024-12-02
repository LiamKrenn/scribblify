from typing import List
from api.model.user import User, UserSchema

from db.session import session
from db.model import UserDB

from crud.utils.hash import hash
from crud.utils.page import pageinate

from sqlalchemy.exc import IntegrityError
from crud.utils.rollback import crud_exception_handle


@crud_exception_handle
def create_user(user: User) -> UserSchema:
    user.password = hash(user.password)
    try:
        db_user = UserDB(**user.model_dump())
        session.add(db_user)
        session.commit()
    except IntegrityError as e:
        raise ValueError("User email already exists")

    return db_user.id


@crud_exception_handle
def authenticate_user(email: str, password: str) -> UserSchema:
    password = hash(password)
    user: UserDB = session.query(UserDB).filter(UserDB.email == email).first()

    if user is None:
        return None

    if user.password != password:
        return None

    return UserSchema.model_validate(user)


@crud_exception_handle
def get_user(email: str) -> UserSchema:
    user: UserDB = session.query(UserDB).filter(UserDB.email == email).first()

    if user is None:
        return None

    return UserSchema.model_validate(user)


@crud_exception_handle
def get_user_ms(oid: str) -> UserSchema:
    user: UserDB = session.query(UserDB).filter(UserDB.ms_oid == oid).first()

    if user is None:
        return None

    return UserSchema.model_validate(user)


@crud_exception_handle
def login_ms(oid: str) -> UserSchema:
    user: UserDB = session.query(UserDB).filter(UserDB.ms_oid == oid).first()

    if user is None:
        return None

    return UserSchema.model_validate(user)


@crud_exception_handle
def create_user_ms(user: User, oid: str) -> UserSchema:
    db_user = UserDB(**user.model_dump(), ms_oid=oid)
    session.add(db_user)
    session.commit()

    return UserSchema.model_validate(db_user)


@crud_exception_handle
def get_users(page: dict) -> List[UserSchema]:
    users = pageinate(session.query(UserDB), page).all()
    return [UserSchema.model_validate(user) for user in users]
