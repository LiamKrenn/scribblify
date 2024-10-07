import os
from typing import Annotated, List
from fastapi import (
    Depends,
    HTTPException,
    status,
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
)

from msal import ConfidentialClientApplication
from msal.authority import (
    AuthorityBuilder,
    AZURE_PUBLIC,
)

from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from api.model.note import Note, NoteSchema
from api.model.page import Page


router = APIRouter(tags=["Security"])

MS_APP_ID = os.getenv("MS_APP_ID")
MS_AUTHORITY_ID = os.getenv("MS_AUTHORITY_ID")
MS_CLIENT_SECRET = os.getenv("MS_CLIENT_SECRET")

authority = AuthorityBuilder(AZURE_PUBLIC, MS_AUTHORITY_ID)
app = ConfidentialClientApplication(
    MS_APP_ID,
    authority=authority,
    client_credential=MS_CLIENT_SECRET,
)


@router.post("/login", status_code=200)
def login(form: OAuth2PasswordRequestForm = Depends()):
    result = app.acquire_token_by_username_password(
        form.username, form.password, scopes=["User.Read"]
    )


@router.post("/logout", status_code=200)
def logout():
    pass


@router.post("/signup", status_code=200)
def signup():
    pass


@router.post("/auth-response", status_code=200)
def auth_response():
    print("auth response")
