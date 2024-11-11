import ssl

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from api import note, security, note_access, tag, user

app = FastAPI()

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain("/secrets/cert.pem", keyfile="/secrets/key.pem")

origins = ["http://localhost:8003", "http://localhost:5173", "http://localhost:3000"]

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
