from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..config import settings
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

router = APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

USERS = {
    "admin": {"username":"admin","password":pwd_context.hash("adminpass"), "role":"admin"},
    "user": {"username":"user","password":pwd_context.hash("userpass"), "role":"user"}
}

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginIn(BaseModel):
    username: str
    password: str

def create_access_token(data: dict, expires_minutes: int):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    encoded = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded

@router.post("/login", response_model=Token)
def login(payload: LoginIn):
    user = USERS.get(payload.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not pwd_context.verify(payload.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user["username"], "role": user["role"]}, settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {"access_token": token, "token_type": "bearer"}
