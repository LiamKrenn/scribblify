from typing import Annotated, List
from fastapi import (
    Depends,
    HTTPException,
    WebSocketException,
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
from api.model.note_command import NoteCommand

import crud.note
from crud.utils.exceptions import UnauthorizedException

from api.utils.security import logged_in_user, ws_logged_in_user
from api.utils.ws import ConnectionManager

SOCKET_MANAGER = ConnectionManager()

router = APIRouter(tags=["Note"])


@router.post("/note", status_code=200, response_model=NoteSchema)
async def create_note(
    note: Note, user: UserSchema = Depends(logged_in_user)
) -> NoteSchema:
    return crud.note.create_note(note, user)


@router.get("/note/{note_id}")
async def get_note_content(
    note_id: int,
    user: UserSchema = Depends(logged_in_user),
):
    try:
        return crud.note.get_note_content(note_id, user)
    except UnauthorizedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.websocket("/ws/{note_id}")
async def note_ws(
    socket: WebSocket,
    note_id: int,
    user: UserSchema = Depends(ws_logged_in_user),
):
    await SOCKET_MANAGER.connect(socket)
    file = crud.note.get_note_file(note_id)
    file.seek(0)

    content = file.read()
    await SOCKET_MANAGER.send(content, socket)
    print(content)

    while True:
        """
        try:
            command = NoteCommand.model_validate_json(await socket.receive_text())
        except ValueError:
            raise WebSocketException(code=status.WS_1007_INVALID_FRAME_PAYLOAD_DATA)

        file.seek(command.cursor)
        file.write(command.char)
        print(command.char)

        await socket.send_text(command.model_dump_json())
        """

        content = await socket.receive_text()
        file.seek(0)
        file.write(content)

        await SOCKET_MANAGER.broadcast(content)


@router.get("/notes", response_model=List[NoteSchema])
async def get_notes(
    page: Annotated[dict, Page] = Depends(Page),
    user: UserSchema = Depends(logged_in_user),
):
    return crud.note.get_notes(page, user)


@router.get("/notes/shared", response_model=List[NoteSchema])
async def get_notes_shared(
    page: Annotated[dict, Page] = Depends(Page),
    user: UserSchema = Depends(logged_in_user),
):
    return crud.note.get_notes_shared(page, user)


@router.delete("/note/{note_id}", status_code=204)
async def delete_note(note_id: int):
    crud.note.delete_note(note_id)
