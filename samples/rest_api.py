"""
Minimal but production-shaped FastAPI service with JWT auth.

Demonstrates: pydantic request/response models, password hashing,
JWT issuance/verification, and a protected route. Drop-in starting point
for "build me a REST API with auth" tasks.

Usage:
    pip install fastapi uvicorn "python-jose[cryptography]" passlib[bcrypt]
    uvicorn rest_api:app --reload
"""
from __future__ import annotations
import os
from datetime import datetime, timedelta, timezone

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel

SECRET = os.getenv("JWT_SECRET", "change-me")
ALGO = "HS256"
TTL_MIN = 60

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2 = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI(title="Sample Auth API")

# Demo store; swap for a real DB.
USERS = {"demo": {"username": "demo", "hash": pwd.hash("demo-pass")}}


class Profile(BaseModel):
    username: str
    issued_at: datetime


def make_token(username: str) -> str:
    exp = datetime.now(timezone.utc) + timedelta(minutes=TTL_MIN)
    return jwt.encode({"sub": username, "exp": exp}, SECRET, algorithm=ALGO)


def current_user(token: str = Depends(oauth2)) -> str:
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGO])
        return payload["sub"]
    except (JWTError, KeyError):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")


@app.post("/token")
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = USERS.get(form.username)
    if not user or not pwd.verify(form.password, user["hash"]):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Bad credentials")
    return {"access_token": make_token(user["username"]), "token_type": "bearer"}


@app.get("/me", response_model=Profile)
def me(username: str = Depends(current_user)):
    return Profile(username=username, issued_at=datetime.now(timezone.utc))
