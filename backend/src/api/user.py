from typing import Annotated, List
from fastapi import (
    Depends,
    HTTPException,
    status,
    APIRouter,
)


from api.model.user import User, UserSchema
from api.model.page import Page
from api.utils.security import logged_in_user

import crud.tag_note
import crud.user


router = APIRouter(prefix="/user", tags=["User"])


@router.get("s", response_model=List[UserSchema])
async def get_users(page: Annotated[dict, Page] = Depends(Page)):
    return crud.user.get_users(page)


@router.get("/me", response_model=UserSchema)
async def get_me(user: User = Depends(logged_in_user)):
    return user


@router.get("", response_model=UserSchema)
async def get_user(email: str, user: User = Depends(logged_in_user)):
    return crud.user.get_user(email)


@router.get("/{user_id}", response_model=UserSchema)
async def get_user(user_id: int):
    return crud.user.get_user(user_id)
