from fastapi import FastAPI
from .routes import auth, analyze, admin
from .models.db import init_db
from .config import settings
import os

app = FastAPI(title="CyberShield - Deepfake Detection Backend")

app.include_router(auth.router)
app.include_router(analyze.router)
app.include_router(admin.router)

@app.on_event("startup")
def startup():
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    init_db()

@app.get("/health")
def health():
    return {"status":"ok"}
