from datetime import datetime, timedelta, timezone
from typing import Union
from fastapi import Depends, HTTPException, Request, WebSocket, WebSocketException
from fastapi.security import OAuth2PasswordBearer
from fastapi import status
from jose import JWTError
import jwt

from api.model.user import UserSchema

import crud
from crud import user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "6b518367b7c9b06c6781ac120d9bc79dc7b1014c52960e8e922758e81f19ff58"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(access_token: str) -> UserSchema:
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        user: UserSchema = crud.user.get_user(email)
    except Exception:
        return None

    return user


def logged_in_user(request: Request) -> UserSchema:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized",
        headers={"WWW-Authenticate": "Bearer"},
    )

    access_token = request.cookies.get("access_token")
    if access_token == None:
        raise credentials_exception

    user = get_current_user(access_token)

    if user is None:
        raise credentials_exception

    return user


def ws_logged_in_user(ws: WebSocket) -> UserSchema:
    credentials_exception = WebSocketException(code=status.WS_1001_GOING_AWAY)

    access_token = ws.cookies.get("access_token")
    if access_token == None:
        raise credentials_exception

    user = get_current_user(access_token)

    if user is None:
        raise credentials_exception

    return user
