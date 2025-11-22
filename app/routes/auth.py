from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.utils.config import settings
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext

router = APIRouter(prefix="/auth", tags=["Authentication"])

# -------------------------------------------------------
# PASSWORD HASHING CONTEXT
# -------------------------------------------------------
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# -------------------------------------------------------
# STATIC USERS (for hackathon/testing only)
# -------------------------------------------------------
USERS = {
    "admin": {
        "username": "admin",
        "password": pwd_context.hash("admin"),  # change after hackathon
        "role": "admin"
    },
    "user": {
        "username": "user",
        "password": pwd_context.hash("userpass"),
        "role": "user"
    }
}

# -------------------------------------------------------
# SCHEMAS
# -------------------------------------------------------
class Token(BaseModel):
    access_token: str
    token_type: str

class LoginIn(BaseModel):
    username: str
    password: str

class UserInfo(BaseModel):
    username: str
    role: str

# -------------------------------------------------------
# TOKEN CREATION
# -------------------------------------------------------
def create_access_token(data: dict, expires_minutes: int):
    """Generate a JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# -------------------------------------------------------
# TOKEN DECODING
# -------------------------------------------------------
def decode_token(token: str):
    """Decode and validate a JWT token."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None

# -------------------------------------------------------
# LOGIN ENDPOINT
# -------------------------------------------------------
@router.post("/login", response_model=Token)
def login(payload: LoginIn):
    """
    Login using username and password.
    Returns an access token if valid.
    """
    user = USERS.get(payload.username)
    if not user or not pwd_context.verify(payload.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token(
        {"sub": user["username"], "role": user["role"]},
        settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    return {"access_token": token, "token_type": "bearer"}

# -------------------------------------------------------
# USER INFO ENDPOINT
# -------------------------------------------------------
@router.get("/me", response_model=UserInfo)
def read_user_me(token: str):
    """
    Decode and return user info from a valid token.
    """
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return {"username": payload["sub"], "role": payload["role"]}
