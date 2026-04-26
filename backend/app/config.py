"""
Configuration settings for PhishPulse backend.
Optimized for resource-constrained environments (7.4GB RAM).
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Project metadata
    PROJECT_NAME: str = "PhishPulse v2.0"
    PROJECT_VERSION: str = "2.0.0"
    PROJECT_DESCRIPTION: str = "Real-Time Multi-Modal Phishing Detection Engine"
    
    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    MODELS_DIR: Path = Field(default=Path("models"))
    DATA_DIR: Path = Field(default=Path("data"))
    REPORTS_DIR: Path = Field(default=Path("reports"))
    
    # Database
    DATABASE_URL: str = "sqlite:///./phishpulse.db"
    DATABASE_ECHO: bool = False
    
    # Security
    SECRET_KEY: str = Field(default="phantomsecdy-research-initiative-secret-key-change-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # CORS
    CORS_ORIGINS: list = Field(default=["*"])
    
    # Rate limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 60  # seconds
    
    # Model A: URL Lexical Analyzer (Isolation Forest)
    URL_MODEL_PATH: str = "models/url_isolation_forest.pkl.gz"
    URL_CONTAMINATION: float = 0.1
    URL_N_ESTIMATORS: int = 100
    URL_MAX_SAMPLES: float = 0.8
    URL_ALEXA_TOP_PATH: str = "data/alexa_top_1m.csv"
    
    # Model B: Email Forensic Analyzer (Naive Bayes)
    EMAIL_MODEL_PATH: str = "models/email_nb_model.pkl"
    EMAIL_VECTORIZER_FEATURES: int = 1024  # Memory-optimized
    
    # Model C: Visual Phishing Detector
    VISUAL_HASHES_DB: str = "models/visual_hashes.db"
    VISUAL_ORB_FEATURES: int = 500
    VISUAL_PHASH_THRESHOLD: int = 10  # Hamming distance threshold
    
    # Model D: Risk Fusion Engine
    URL_WEIGHT: float = 0.30
    EMAIL_WEIGHT: float = 0.35
    VISUAL_WEIGHT: float = 0.35
    
    # Risk thresholds
    THRESHOLD_CLEAN: int = 30
    THRESHOLD_SUSPICIOUS: int = 60
    THRESHOLD_MALICIOUS: int = 85
    THRESHOLD_CRITICAL: int = 100
    
    # Domain age penalty
    DOMAIN_AGE_PENALTY: int = 20  # Added to score if domain < 7 days
    DOMAIN_AGE_DAYS: int = 7
    
    # SSL penalty
    SSL_INVALID_PENALTY: int = 15
    
    # Suspicious TLDs with risk scores
    SUSPICIOUS_TLDS: dict = Field(default={
        ".tk": 15,
        ".ml": 15,
        ".cf": 15,
        ".ga": 15,
        ".gq": 15,
        ".xyz": 10,
        ".top": 10,
        ".work": 8,
        ".date": 8,
        ".racing": 8,
        ".loan": 10,
        ".download": 8,
        ".stream": 8,
        ".bid": 8,
        ".review": 8,
        ".party": 8,
        ".trade": 8,
        ".science": 8,
        ".ninja": 5,
        ".click": 8,
        ".link": 5,
    })
    
    # Email urgency keywords
    URGENCY_KEYWORDS: list = Field(default=[
        "immediate action", "verify now", "account suspended", "urgent",
        "limited time", "act now", "click here", "update required",
        "verify your account", "confirm your identity", "suspended",
        "unauthorized access", "security alert", "password expired",
        "account locked", "verify immediately"
    ])
    
    # API endpoints
    API_V1_STR: str = "/api/v1"
    
    # External APIs
    PHISHTANK_API_URL: str = "http://data.phishtank.com/data/online-valid.json"
    
    # Screenshot service
    SCREENSHOT_TIMEOUT: int = 10000  # milliseconds
    SCREENSHOT_VIEWPORT: dict = Field(default={"width": 1920, "height": 1080})
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings."""
    return settings
