from pydantic import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "replace-with-strong-secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60*24
    DATABASE_URL: str = "sqlite:///./app.db"
    UPLOAD_DIR: str = "./uploads"
    ML_MODEL_PATH: str = "./app/ml_core/models/xception_ffpp.pth"
    ENABLE_DEEPFACELIVE: bool = False

settings = Settings()
