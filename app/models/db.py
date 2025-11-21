from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
from ..config import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ScanResult(Base):
    __tablename__ = "scan_results"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    user = Column(String, default="anonymous")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    authenticity_score = Column(Float, default=0.0)
    is_fake = Column(Integer, default=0)
    report = Column(JSON, nullable=True)

def init_db():
    Base.metadata.create_all(bind=engine)
