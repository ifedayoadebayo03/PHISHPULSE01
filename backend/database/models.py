"""
SQLAlchemy database models for PhishPulse.
"""

import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, String, Integer, Float, DateTime, Text, JSON, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.config import settings

Base = declarative_base()


class Scan(Base):
    """Scan result model."""
    __tablename__ = "scans"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, default=datetime.utcnow)
    scan_type = Column(String, nullable=False)  # 'url', 'email', 'visual'
    target = Column(String, nullable=False)  # URL, email subject, or image path
    
    # Risk scores
    final_score = Column(Integer, nullable=False)
    classification = Column(String, nullable=False)  # 'Clean', 'Suspicious', 'Malicious', 'Critical'
    confidence_lower = Column(Float)
    confidence_upper = Column(Float)
    
    # Model breakdown (JSON)
    url_score = Column(Integer, nullable=True)
    email_score = Column(Integer, nullable=True)
    visual_score = Column(Integer, nullable=True)
    
    # Indicators and mitigation
    indicators = Column(JSON, default=list)
    mitigation_steps = Column(JSON, default=list)
    
    # Additional metadata
    domain_age_days = Column(Integer, nullable=True)
    has_valid_ssl = Column(Boolean, nullable=True)
    impersonated_brand = Column(String, nullable=True)
    
    # Report
    report_generated = Column(Boolean, default=False)
    report_path = Column(String, nullable=True)
    
    def __repr__(self):
        return f"<Scan(id={self.id}, type={self.scan_type}, score={self.final_score})>"


class Report(Base):
    """Generated forensic report model."""
    __tablename__ = "reports"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    scan_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer)
    
    def __repr__(self):
        return f"<Report(id={self.id}, scan_id={self.scan_id})>"


class URLFeature(Base):
    """URL feature extraction cache."""
    __tablename__ = "url_features"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    url = Column(String, nullable=False, unique=True)
    entropy = Column(Float)
    levenshtein_distance = Column(Integer)
    subdomain_depth = Column(Integer)
    tld_risk = Column(Integer)
    has_suspicious_keywords = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow)


class EmailFeature(Base):
    """Email feature extraction cache."""
    __tablename__ = "email_features"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email_hash = Column(String, nullable=False, unique=True)  # SHA256 of email content
    spf_aligned = Column(Boolean)
    dkim_aligned = Column(Boolean)
    dmarc_aligned = Column(Boolean)
    return_path_match = Column(Boolean)
    urgency_score = Column(Float)
    html_text_ratio = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


class VisualHash(Base):
    """Visual perceptual hash database."""
    __tablename__ = "visual_hashes"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    brand_name = Column(String, nullable=False)
    phash = Column(String, nullable=False)  # 64-bit pHash as hex string
    image_path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


# Database engine and session
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    poolclass=StaticPool if "sqlite" in settings.DATABASE_URL else None,
    echo=settings.DATABASE_ECHO
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
