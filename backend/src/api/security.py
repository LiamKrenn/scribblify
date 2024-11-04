from datetime import datetime, timedelta, timezone
import os
from typing import Annotated, List
from fastapi import (
    Depends,
    HTTPException,
    Request,
    Response,
    status,
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
)


from jose import JWTError
from msal import ConfidentialClientApplication
from msal.oauth2cli.oidc import decode_id_token
from msal.authority import (
    AuthorityBuilder,
    AZURE_PUBLIC,
)

from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer

from jwt import PyJWKClient

from api.model.user import User, UserSchema
from api.model.token import Token

from expiring_dict import ExpiringDict

from api.utils.security import logged_in_user, create_access_token
import crud
from crud import user
import crud.user


router = APIRouter(tags=["Security"])

MS_APP_ID = os.getenv("MS_APP_ID")
# tenant id
MS_AUTHORITY_ID = os.getenv("MS_AUTHORITY_ID")
MS_CLIENT_SECRET = os.getenv("MS_CLIENT_SECRET")

authority = AuthorityBuilder(AZURE_PUBLIC, MS_AUTHORITY_ID)
app = ConfidentialClientApplication(
    MS_APP_ID,
    authority=authority,
    client_credential=MS_CLIENT_SECRET,
)

jwk = PyJWKClient(
    f"https://login.microsoftonline.com/{MS_AUTHORITY_ID}/discovery/v2.0/keys"
)

oauth_cache = ExpiringDict(60)  # Keys will exist for 60 seconds


@router.get("/login/oauth/ms")
def login():
    result = app.initiate_auth_code_flow(["User.Read"])
    oauth_cache[result["state"]] = result
    print(result)
    return RedirectResponse(result["auth_uri"])


@router.post("/login/ms", status_code=200)
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    result = app.acquire_token_by_username_password(
        form.username, form.password, ["User.Read"]
    )
    if result.get("error") is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = crud.user.get_user_ms(result["id_token_claims"]["oid"])
    if user is None:
        user = crud.user.create_user_ms(
            User(email=result["id_token_claims"]["preferred_username"]),
            result["id_token_claims"]["oid"],
        )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(data={"sub": user.email})
    response = RedirectResponse(
        url="http://localhost:5173", status_code=status.HTTP_200_OK
    )
    response.set_cookie("access_token", value=f"{token}", httponly=True, secure=True)

    return response


@router.post("/login", status_code=200)
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = crud.user.authenticate_user(form.username, form.password)
    token = create_access_token(data={"sub": user.email})

    response = RedirectResponse(
        url="http://localhost:5173", status_code=status.HTTP_200_OK
    )
    response.set_cookie("access_token", value=f"{token}", httponly=True, secure=True)

    return response


@router.post("/logout", status_code=200)
def logout(current_user: Annotated[UserSchema, Depends(logged_in_user)]):
    app.remove_account()


@router.post("/signup", status_code=200)
def signup(user: User):
    return crud.user.create_user(user)


@router.get("/auth-response", status_code=200)
def oauth_redirect(request: Request):
    query = dict(request.query_params)

    auth_code_flow = oauth_cache.pop(query["state"])
    result = app.acquire_token_by_auth_code_flow(auth_code_flow, query)

    user = crud.user.get_user_ms(result["id_token_claims"]["oid"])

    token = create_access_token(data={"sub": user.email})
    response = RedirectResponse(
        url="http://localhost:5173", status_code=status.HTTP_200_OK
    )
    response.set_cookie("access_token", value=f"{token}", httponly=True, secure=True)

    return response
