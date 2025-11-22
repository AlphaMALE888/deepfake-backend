from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime
from ..utils.config import settings

# -------------------------------------------------------
# DATABASE ENGINE
# -------------------------------------------------------
try:
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False}  # Required for SQLite + FastAPI
    )
    print(f"[DB] Connected successfully → {settings.DATABASE_URL}")
except Exception as e:
    print("[DB ERROR] Failed to initialize engine:", e)
    engine = None

# -------------------------------------------------------
# SESSION FACTORY
# -------------------------------------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# -------------------------------------------------------
# BASE CLASS
# -------------------------------------------------------
Base = declarative_base()

# -------------------------------------------------------
# DATABASE MODELS
# -------------------------------------------------------
class ScanResult(Base):
    """
    Stores the results of deepfake analysis for video/image/audio uploads.
    """
    __tablename__ = "scan_results"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    user = Column(String, default="anonymous")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    authenticity_score = Column(Float, default=0.0)
    is_fake = Column(Integer, default=0)
    report = Column(JSON, nullable=True)

    def __repr__(self):
        return f"<ScanResult(filename={self.filename}, score={self.authenticity_score}, fake={self.is_fake})>"


# -------------------------------------------------------
# UTILITY: GET DB SESSION
# -------------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------------------------------------
# INITIALIZE DATABASE
# -------------------------------------------------------
def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        print("[DB] Tables created successfully.")
    except Exception as e:
        print("[DB ERROR] Failed to create tables:", e)
