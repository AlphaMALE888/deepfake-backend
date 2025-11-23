from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.routes import auth, analyze, admin
from app.models.db import init_db
from app.utils.config import settings
from fastapi.staticfiles import StaticFiles




# ---------------------------------------------------
# APP INITIALIZATION
# ---------------------------------------------------
app = FastAPI(
    title="CyberShield - Deepfake Detection Backend",
    version="2.0.0",
    description=(
        "AI-powered backend for detecting deepfake videos, "
        "images, and audio using Hugging Face models."
    ),
)


# ---------------------------------------------------
# CORS MIDDLEWARE (FOR FRONTEND INTEGRATION)
# ---------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict later for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------
# ROUTE REGISTRATION
# ---------------------------------------------------
app.include_router(auth.router)
app.include_router(analyze.router)
app.include_router(admin.router)


# ---------------------------------------------------
# STARTUP EVENTS
# ---------------------------------------------------
@app.on_event("startup")
def on_startup():
    """Initialize database and directories."""
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    init_db()
    print("🔥 CyberShield backend started successfully!")


# ---------------------------------------------------
# HEALTH CHECK ENDPOINT
# ---------------------------------------------------
@app.get("/health", tags=["system"])
def health_check():
    """
    Quick system health check endpoint.
    Returns:
        JSON indicating if the backend is live and responsive.
    """
    return {
        "status": "ok",
        "service": "CyberShield Deepfake Detector",
        "model": settings.HF_DEEPFAKE_MODEL,
        "upload_dir": settings.UPLOAD_DIR,
    }

app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")
