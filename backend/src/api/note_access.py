from typing import Annotated, List
from fastapi import (
    Depends,
    HTTPException,
    status,
    APIRouter,
)


from api.model.note_access import NoteAccess
from api.model.page import Page

import crud.note_access


router = APIRouter(prefix="/note_access", tags=["Note Access"])


@router.post("", status_code=204)
async def add_note_access(note_access: NoteAccess):
    crud.note_access.add_note_access(note_access)


@router.get("/{note_id}", response_model=List[NoteAccess])
async def get_note_access(note_id: int):
    return crud.note_access.get_note_access(note_id)


@router.delete("/{note_id}/{user_id}", status_code=204)
async def delete_note_access(note_id: int, user_id: int):
    crud.note_access.delete_note_access(note_id, user_id)
