"""
CRUD operations for PhishPulse database.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime, timedelta

from backend.database.models import Scan, Report, URLFeature, EmailFeature, VisualHash


# Scan operations
def create_scan(db: Session, scan_data: dict) -> Scan:
    """Create a new scan record."""
    db_scan = Scan(**scan_data)
    db.add(db_scan)
    db.commit()
    db.refresh(db_scan)
    return db_scan


def get_scan(db: Session, scan_id: str) -> Optional[Scan]:
    """Get scan by ID."""
    return db.query(Scan).filter(Scan.id == scan_id).first()


def get_scans(db: Session, skip: int = 0, limit: int = 100) -> List[Scan]:
    """Get all scans with pagination."""
    return db.query(Scan).order_by(desc(Scan.timestamp)).offset(skip).limit(limit).all()


def get_recent_scans(db: Session, hours: int = 24) -> List[Scan]:
    """Get scans from last N hours."""
    cutoff = datetime.utcnow() - timedelta(hours=hours)
    return db.query(Scan).filter(Scan.timestamp >= cutoff).all()


def get_scans_by_classification(db: Session, classification: str) -> List[Scan]:
    """Get scans by classification."""
    return db.query(Scan).filter(Scan.classification == classification).all()


def update_scan(db: Session, scan_id: str, update_data: dict) -> Optional[Scan]:
    """Update scan record."""
    db_scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if db_scan:
        for key, value in update_data.items():
            setattr(db_scan, key, value)
        db.commit()
        db.refresh(db_scan)
    return db_scan


# Report operations
def create_report(db: Session, report_data: dict) -> Report:
    """Create a new report record."""
    db_report = Report(**report_data)
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report


def get_report(db: Session, report_id: str) -> Optional[Report]:
    """Get report by ID."""
    return db.query(Report).filter(Report.id == report_id).first()


def get_report_by_scan(db: Session, scan_id: str) -> Optional[Report]:
    """Get report by scan ID."""
    return db.query(Report).filter(Report.scan_id == scan_id).first()


# URL Feature operations
def get_url_feature(db: Session, url: str) -> Optional[URLFeature]:
    """Get cached URL features."""
    return db.query(URLFeature).filter(URLFeature.url == url).first()


def create_url_feature(db: Session, feature_data: dict) -> URLFeature:
    """Create URL feature cache entry."""
    db_feature = URLFeature(**feature_data)
    db.add(db_feature)
    db.commit()
    db.refresh(db_feature)
    return db_feature


# Email Feature operations
def get_email_feature(db: Session, email_hash: str) -> Optional[EmailFeature]:
    """Get cached email features."""
    return db.query(EmailFeature).filter(EmailFeature.email_hash == email_hash).first()


def create_email_feature(db: Session, feature_data: dict) -> EmailFeature:
    """Create email feature cache entry."""
    db_feature = EmailFeature(**feature_data)
    db.add(db_feature)
    db.commit()
    db.refresh(db_feature)
    return db_feature


# Visual Hash operations
def get_visual_hashes(db: Session, brand_name: Optional[str] = None) -> List[VisualHash]:
    """Get visual hashes, optionally filtered by brand."""
    query = db.query(VisualHash)
    if brand_name:
        query = query.filter(VisualHash.brand_name == brand_name)
    return query.all()


def create_visual_hash(db: Session, hash_data: dict) -> VisualHash:
    """Create visual hash entry."""
    db_hash = VisualHash(**hash_data)
    db.add(db_hash)
    db.commit()
    db.refresh(db_hash)
    return db_hash


def delete_visual_hash(db: Session, hash_id: str) -> bool:
    """Delete visual hash entry."""
    db_hash = db.query(VisualHash).filter(VisualHash.id == hash_id).first()
    if db_hash:
        db.delete(db_hash)
        db.commit()
        return True
    return False


# Statistics
def get_scan_statistics(db: Session) -> dict:
    """Get scan statistics."""
    total = db.query(Scan).count()
    clean = db.query(Scan).filter(Scan.classification == "Clean").count()
    suspicious = db.query(Scan).filter(Scan.classification == "Suspicious").count()
    malicious = db.query(Scan).filter(Scan.classification == "Malicious").count()
    critical = db.query(Scan).filter(Scan.classification == "Critical").count()
    
    # Last 24 hours
    day_ago = datetime.utcnow() - timedelta(hours=24)
    last_24h = db.query(Scan).filter(Scan.timestamp >= day_ago).count()
    
    # Average risk score
    from sqlalchemy import func
    avg_score = db.query(func.avg(Scan.final_score)).scalar() or 0
    
    return {
        "total_scans": total,
        "clean_count": clean,
        "suspicious_count": suspicious,
        "malicious_count": malicious,
        "critical_count": critical,
        "last_24h_scans": last_24h,
        "average_risk_score": round(float(avg_score), 2)
    }
