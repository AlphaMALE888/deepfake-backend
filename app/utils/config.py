from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    # ------------------------------
    # SECURITY SETTINGS
    # ------------------------------
    SECRET_KEY: str = "super-strong-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    # ------------------------------
    # DATABASE
    # ------------------------------
    DATABASE_URL: str = "sqlite:///./app.db"

    # ------------------------------
    # UPLOADS
    # ------------------------------
    UPLOAD_DIR: str = "./uploads"

    # ------------------------------
    # HUGGINGFACE API MODEL SETTINGS
    # (Works with HF API models)
    # ------------------------------
    HF_DEEPFAKE_MODEL: str = "umarbutler/deepfake-detection"   # working deepfake model
    HF_TOKEN: str = "hf_XXXXXXXXXXXXXXXXXXXXXXXX"
         # set your API token here or in env

    # ------------------------------
    # UNUSED OLD FIELDS (REMOVED)
    # ML_MODEL_PATH deleted because you switched to HF API
    # ENABLE_DEEPFACELIVE removed
    # ------------------------------

    class Config:
        env_file = ".env"


settings = Settings()
