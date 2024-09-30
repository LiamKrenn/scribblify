from typing import Annotated
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

import crud.note


router = APIRouter(prefix="/note", tags=["Note"])


@router.post("", status_code=200)
async def create_note(note: Note) -> NoteSchema:
    return crud.note.create_note(note)


@router.websocket("/ws/{note_id}")
async def note_ws(socket: WebSocket, note_id: int):
    await socket.accept()
    
    while True:
        data = await socket.receive_text()
        print(data)
