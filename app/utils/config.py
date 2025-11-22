from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    """
    Global application configuration class.
    Automatically loads values from environment variables or .env file.
    """

    # ---------------------------------------------------
    # SECURITY SETTINGS
    # ---------------------------------------------------
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-strong-secret-key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24))

    # ---------------------------------------------------
    # DATABASE
    # ---------------------------------------------------
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")

    # ---------------------------------------------------
    # UPLOADS DIRECTORY
    # ---------------------------------------------------
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")

    # ---------------------------------------------------
    # HUGGING FACE MODEL SETTINGS
    # ---------------------------------------------------
    HF_DEEPFAKE_MODEL: str = os.getenv("HF_DEEPFAKE_MODEL", "umarbutler/deepfake-detection")
    HF_TOKEN: str = os.getenv("HF_TOKEN", "hf_XXXXXXXXXXXXXXXXXXXXXXXX")

    # ---------------------------------------------------
    # OPTIONAL PERFORMANCE SETTINGS
    # ---------------------------------------------------
    MAX_VIDEO_SIZE_MB: int = int(os.getenv("MAX_VIDEO_SIZE_MB", 500))  # optional limit
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# ✅ Instantiate global settings
settings = Settings()

