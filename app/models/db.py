from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime
from ..utils.config import settings

# ------------------------------
# DATABASE ENGINE
# ------------------------------
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}  # required for SQLite in FastAPI threads
)

# ------------------------------
# SESSION FACTORY
# ------------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ------------------------------
# BASE CLASS
# ------------------------------
Base = declarative_base()

# ------------------------------
# DATABASE MODELS
# ------------------------------
class ScanResult(Base):
    __tablename__ = "scan_results"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    user = Column(String, default="anonymous")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    authenticity_score = Column(Float, default=0.0)
    is_fake = Column(Integer, default=0)
    report = Column(JSON, nullable=True)


# ------------------------------
# UTILITY: GET DB SESSION
# ------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------------------
# INITIALIZE DB
# ------------------------------
def init_db():
    Base.metadata.create_all(bind=engine)

