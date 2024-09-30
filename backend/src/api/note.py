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

import crud.note


router = APIRouter(tags=["Note"])


@router.post("/note", status_code=200)
async def create_note(note: Note) -> NoteSchema:
    return crud.note.create_note(note)


@router.websocket("/ws/{note_id}")
async def note_ws(socket: WebSocket, note_id: int):
    await socket.accept()

    while True:
        data = await socket.receive_text()
        print(data)


@router.get("/notes", response_model=List[NoteSchema])
async def get_notes(page: Annotated[dict, Page] = Depends(Page)):
    return crud.note.get_notes(page)
