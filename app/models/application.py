from sqlalchemy import Column, Integer, String, Float, Text, DateTime, JSON, Enum
from sqlalchemy.sql import func
from app.db import Base
import enum

class ApplicationStatus(str, enum.Enum):
    applied = "applied"
    interviewing = "interviewing"
    offered = "offered"
    rejected = "rejected"

class Application(Base):
    __tablename__ = "applications"

    id              = Column(Integer, primary_key=True)
    company         = Column(String(255), nullable=False)
    role            = Column(String(255), nullable=False)
    raw_jd          = Column(Text, nullable=False)
    required_skills = Column(JSON, nullable=True)      # ← list stored as JSON
    seniority       = Column(String(50), nullable=True)
    salary_min      = Column(Integer, nullable=True)
    salary_max      = Column(Integer, nullable=True)
    status          = Column(Enum(ApplicationStatus), default=ApplicationStatus.applied)
    match_score     = Column(Float, nullable=True)
    match_reasoning = Column(Text, nullable=True)
    created_at      = Column(DateTime(timezone=True), server_default=func.now())