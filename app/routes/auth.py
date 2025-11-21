from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.utils.config import settings
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# ---------------------------------------------------
# HARDCODED USERS (STATIC HASHES FOR STABILITY)
# ---------------------------------------------------
USERS = {
    "admin": {
        "username": "admin",
        "password": pwd_context.hash("admin"),   # for hackathon only
        "role": "admin"
    },
    "user": {
        "username": "user",
        "password": pwd_context.hash("userpass"),
        "role": "user"
    }
}

# ---------------------------------------------------
# SCHEMAS
# ---------------------------------------------------
class Token(BaseModel):
    access_token: str
    token_type: str

class LoginIn(BaseModel):
    username: str
    password: str

# ---------------------------------------------------
# TOKEN CREATION
# ---------------------------------------------------
def create_access_token(data: dict, expires_minutes: int):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

# ---------------------------------------------------
# LOGIN ENDPOINT
# ---------------------------------------------------
@router.post("/login", response_model=Token)
def login(payload: LoginIn):
    user = USERS.get(payload.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not pwd_context.verify(payload.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        {"sub": user["username"], "role": user["role"]},
        settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    return {"access_token": token, "token_type": "bearer"}

# ---------------------------------------------------
# OPTIONAL: Who Am I (for frontend convenience)
# ---------------------------------------------------
class UserInfo(BaseModel):
    username: str
    role: str

def decode_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None

@router.get("/me", response_model=UserInfo)
def read_user_me(token: str):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return {
        "username": payload["sub"],
        "role": payload["role"]
    }
