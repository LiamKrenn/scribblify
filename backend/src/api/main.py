import os
import ssl

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from api import note, security, note_access, tag, user

app = FastAPI()

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain("/secrets/cert.pem", keyfile="/secrets/key.pem")

origins = []
FRONTEND_URL = os.getenv("FRONTEND_URL")
if FRONTEND_URL:
    origins.append(FRONTEND_URL)
else:
    raise ValueError("FRONTEND_URL environment variable not set")


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routers
app.include_router(note.router)
app.include_router(security.router)
app.include_router(note_access.router)
app.include_router(tag.router)
app.include_router(user.router)
