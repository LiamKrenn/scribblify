from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
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


def logged_in_user(access_token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception

        user: UserSchema = crud.user.get_user(email)
        if user is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    return user
