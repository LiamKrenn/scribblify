from typing import Annotated, List
from fastapi import (
    Depends,
    HTTPException,
    status,
    APIRouter,
)


from api.model.tag import Tag, TagSchema
from api.model.page import Page

import crud.tag_note


router = APIRouter(prefix="/tag", tags=["Tag"])


@router.post("/{note_id}/{tag_id}", status_code=204)
async def add_tag(note_id: int, tag_id: int):
    crud.tag_note.add_note_tag(tag_id, note_id)


@router.delete("/{note_id}/{tag_id}", status_code=204)
async def delete_tag(note_id: int, tag_id: int):
    crud.tag_note.delete_note_tag(tag_id, note_id)
