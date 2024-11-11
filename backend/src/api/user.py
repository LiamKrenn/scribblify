from typing import Annotated, List
from fastapi import (
    Depends,
    HTTPException,
    status,
    APIRouter,
)


from api.model.user import User, UserPublic, UserSchema
from api.model.page import Page
from api.utils.security import logged_in_user

import crud.tag_note
import crud.user


router = APIRouter(prefix="/user", tags=["User"])


@router.get("s", response_model=List[UserPublic])
async def get_users(page: Annotated[dict, Page] = Depends(Page)):
    return crud.user.get_users(page)


@router.get("/me", response_model=UserPublic)
async def get_me(user: UserSchema = Depends(logged_in_user)):
    return user


@router.get("", response_model=UserPublic)
async def get_user(email: str, user: UserSchema = Depends(logged_in_user)):
    user = crud.user.get_user(email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/{user_id}", response_model=UserPublic)
async def get_user(user_id: int):
    user = crud.user.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
