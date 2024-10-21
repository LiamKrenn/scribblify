from typing import Annotated, List
from fastapi import (
    Depends,
    HTTPException,
    status,
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from api.model.note import Note, NoteSchema
from api.model.page import Page

from api.model.user import UserSchema
import crud.note

from api.utils.security import logged_in_user


router = APIRouter(tags=["Note"])


@router.post("/note", status_code=200)
async def create_note(
    note: Note, user: UserSchema = Depends(logged_in_user)
) -> NoteSchema:
    return crud.note.create_note(note, user)


@router.websocket("/ws/{note_id}")
async def note_ws(socket: WebSocket, note_id: int):
    await socket.accept()
    file = crud.note.get_note_file(note_id)

    while True:
        data = await socket.receive_text()
        file.write(data)
        socket.send_text(data)


@router.get("/notes", response_model=List[NoteSchema])
async def get_notes(
    page: Annotated[dict, Page] = Depends(Page),
    user: UserSchema = Depends(logged_in_user),
):
    return crud.note.get_notes(page, user)


@router.delete("/note/{note_id}", status_code=204)
async def delete_note(note_id: int):
    crud.note.delete_note(note_id)
