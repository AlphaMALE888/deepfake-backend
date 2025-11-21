from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth, analyze, admin
from app.models.db import init_db
from app.utils.config import settings

import os

# ---------------------------------------------------
# APP INITIALIZATION
# ---------------------------------------------------
app = FastAPI(
    title="CyberShield - Deepfake Detection Backend",
    version="1.0.0"
)

# ---------------------------------------------------
# ENABLE CORS (IMPORTANT FOR FRONTEND)
# ---------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------
# INCLUDE ROUTERS
# ---------------------------------------------------
app.include_router(auth.router)
app.include_router(analyze.router)
app.include_router(admin.router)

# ---------------------------------------------------
# STARTUP EVENTS
# ---------------------------------------------------
@app.on_event("startup")
def startup():
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    init_db()
    print("🔥 Backend started successfully!")


# ---------------------------------------------------
# HEALTH CHECK ENDPOINT
# ---------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok", "message": "CyberShield backend running smoothly"}

