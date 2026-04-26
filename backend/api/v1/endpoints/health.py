"""
Health check and system status endpoints.
"""

import os
import sys
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.models import get_db
from backend.database import crud
from backend.app.config import settings
from backend.scanners import (
    URLLexicalAnalyzer,
    EmailForensicAnalyzer,
    VisualPhishingDetector,
    RiskFusionEngine
)

router = APIRouter()

# Initialize scanners to check status
url_analyzer = URLLexicalAnalyzer()
email_analyzer = EmailForensicAnalyzer()
visual_detector = VisualPhishingDetector()
risk_fusion = RiskFusionEngine()


@router.get("/")
async def health_check():
    """Basic health check."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.PROJECT_VERSION
    }


@router.get("/detailed")
async def detailed_health(db: Session = Depends(get_db)):
    """Detailed system health check."""
    # Check model status
    models_status = {
        "url_lexical_analyzer": {
            "loaded": url_analyzer.is_fitted,
            "algorithm": "Isolation Forest"
        },
        "email_forensic_analyzer": {
            "loaded": email_analyzer.is_fitted,
            "algorithm": "Multinomial Naive Bayes"
        },
        "visual_phishing_detector": {
            "loaded": len(visual_detector.brand_hashes) > 0,
            "brand_count": sum(len(v) for v in visual_detector.brand_hashes.values()),
            "algorithm": "ORB + Perceptual Hashing"
        },
        "risk_fusion_engine": {
            "loaded": True,
            "algorithm": "Weighted Ensemble + Isotonic Regression"
        }
    }
    
    # Check directories
    dirs_status = {
        "models_dir": os.path.exists(settings.MODELS_DIR),
        "data_dir": os.path.exists(settings.DATA_DIR),
        "reports_dir": os.path.exists(settings.REPORTS_DIR)
    }
    
    # Get database stats
    try:
        stats = crud.get_scan_statistics(db)
    except Exception as e:
        stats = {"error": str(e)}
    
    # Python version
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.PROJECT_VERSION,
        "python_version": python_version,
        "models": models_status,
        "directories": dirs_status,
        "database": stats
    }


@router.get("/statistics")
async def get_statistics(db: Session = Depends(get_db)):
    """Get scan statistics."""
    stats = crud.get_scan_statistics(db)
    return stats


@router.get("/model-info")
async def model_info():
    """Get information about all models."""
    return {
        "models": [
            {
                "name": "URL Lexical Analyzer (Model A)",
                "type": "Unsupervised",
                "algorithm": "Isolation Forest + Regex Heuristics",
                "features": [
                    "Shannon Entropy (DGA detection)",
                    "Levenshtein Distance (typosquatting)",
                    "Suspicious TLD scoring",
                    "Subdomain depth analysis"
                ],
                "weight": settings.URL_WEIGHT,
                "status": "loaded" if url_analyzer.is_fitted else "untrained"
            },
            {
                "name": "Email Forensic Analyzer (Model B)",
                "type": "Supervised",
                "algorithm": "TF-IDF + Multinomial Naive Bayes",
                "features": [
                    "SPF/DKIM/DMARC validation",
                    "Return-Path analysis",
                    "Urgency keyword detection",
                    "HTML/Text ratio analysis"
                ],
                "weight": settings.EMAIL_WEIGHT,
                "status": "loaded" if email_analyzer.is_fitted else "untrained"
            },
            {
                "name": "Visual Phishing Detector (Model C)",
                "type": "Unsupervised",
                "algorithm": "ORB + Perceptual Hashing (pHash)",
                "features": [
                    "ORB feature extraction",
                    "Perceptual hash comparison",
                    "Form field detection",
                    "SSL badge spoofing detection"
                ],
                "weight": settings.VISUAL_WEIGHT,
                "status": "loaded" if len(visual_detector.brand_hashes) > 0 else "untrained",
                "brand_hashes": sum(len(v) for v in visual_detector.brand_hashes.values())
            },
            {
                "name": "Risk Fusion Engine (Model D)",
                "type": "Meta-Classifier",
                "algorithm": "Weighted Voting + Isotonic Regression",
                "features": [
                    "Multi-modal signal aggregation",
                    "Dynamic risk adjustments",
                    "Confidence interval calculation",
                    "Calibrated probability output"
                ],
                "weight": "N/A",
                "status": "loaded"
            }
        ],
        "thresholds": {
            "clean": f"0-{settings.THRESHOLD_CLEAN}",
            "suspicious": f"{settings.THRESHOLD_CLEAN+1}-{settings.THRESHOLD_SUSPICIOUS}",
            "malicious": f"{settings.THRESHOLD_SUSPICIOUS+1}-{settings.THRESHOLD_MALICIOUS}",
            "critical": f"{settings.THRESHOLD_MALICIOUS+1}-{settings.THRESHOLD_CRITICAL}"
        }
    }
