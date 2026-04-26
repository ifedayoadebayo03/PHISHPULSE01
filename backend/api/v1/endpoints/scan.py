"""
Scan endpoint - orchestrates all 4 models.
"""

import uuid
import base64
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from urllib.parse import urlparse
import tldextract

from backend.database.models import get_db
from backend.database import crud
from backend.scanners import (
    URLLexicalAnalyzer,
    EmailForensicAnalyzer,
    VisualPhishingDetector,
    RiskFusionEngine
)
from backend.services.whois_lookup import WHOISLookup
from backend.services.screenshot_service import ScreenshotService
from backend.services.pdf_generator import ForensicReportGenerator

router = APIRouter()

# Initialize scanners
url_analyzer = URLLexicalAnalyzer()
email_analyzer = EmailForensicAnalyzer()
visual_detector = VisualPhishingDetector()
risk_fusion = RiskFusionEngine()
whois_service = WHOISLookup()


class ScanRequest(BaseModel):
    """Scan request model."""
    type: str = Field(..., description="Scan type: 'url', 'email', or 'visual'")
    target: str = Field(..., description="URL, email content, or base64 image")
    headers: Optional[str] = Field(None, description="Email headers (for email scans)")
    options: Optional[dict] = Field(default_factory=dict, description="Scan options")


class ScanResponse(BaseModel):
    """Scan response model."""
    scan_id: str
    timestamp: str
    scan_type: str
    target: str
    final_score: int
    classification: str
    confidence_interval: List[float]
    model_breakdown: dict
    indicators: list
    mitigation_steps: list
    report_url: Optional[str] = None


@router.post("/", response_model=ScanResponse)
async def create_scan(
    request: ScanRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Create a new scan using all 4 models.
    
    - **type**: Scan type ('url', 'email', or 'visual')
    - **target**: URL, email content, or base64 image
    - **headers**: Optional email headers
    - **options**: Additional scan options (screenshot, generate_report)
    """
    scan_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()
    
    # Initialize results
    url_result = None
    email_result = None
    visual_result = None
    domain_age_days = None
    has_valid_ssl = None
    screenshot_path = None
    
    try:
        if request.type == "url":
            # URL scan
            url_result = url_analyzer.analyze(request.target)
            
            # Get domain info
            extracted = tldextract.extract(request.target)
            domain = f"{extracted.domain}.{extracted.suffix}"
            
            whois_info = whois_service.lookup(domain)
            domain_age_days = whois_info.get('domain_age_days')
            
            ssl_info = whois_service.get_ssl_info(domain)
            has_valid_ssl = ssl_info.get('has_ssl')
            
            # Screenshot if requested
            if request.options.get('screenshot', False):
                screenshot_service = ScreenshotService()
                screenshot_data = screenshot_service.capture_sync(request.target)
                screenshot_path = screenshot_data.get('screenshot_path')
            
        elif request.type == "email":
            # Email scan
            email_result = email_analyzer.analyze(request.target, request.headers)
            
        elif request.type == "visual":
            # Visual scan
            image_bytes = base64.b64decode(request.target)
            visual_result = visual_detector.analyze_bytes(image_bytes)
            
        else:
            raise HTTPException(status_code=400, detail=f"Invalid scan type: {request.type}")
        
        # Fuse results
        fusion_result = risk_fusion.fuse(
            url_result=url_result,
            email_result=email_result,
            visual_result=visual_result,
            domain_age_days=domain_age_days,
            has_valid_ssl=has_valid_ssl
        )
        
        # Prepare scan data
        scan_data = {
            "id": scan_id,
            "timestamp": datetime.utcnow(),
            "scan_type": request.type,
            "target": request.target[:500],  # Truncate for DB storage
            "final_score": fusion_result["final_score"],
            "classification": fusion_result["classification"],
            "confidence_lower": fusion_result["confidence_interval"][0],
            "confidence_upper": fusion_result["confidence_interval"][1],
            "url_score": url_result["score"] if url_result else None,
            "email_score": email_result["score"] if email_result else None,
            "visual_score": visual_result["score"] if visual_result else None,
            "indicators": fusion_result["indicators"],
            "mitigation_steps": fusion_result["mitigation_steps"],
            "domain_age_days": domain_age_days,
            "has_valid_ssl": has_valid_ssl,
            "impersonated_brand": fusion_result.get("impersonated_brand"),
        }
        
        # Save to database
        crud.create_scan(db, scan_data)
        
        # Generate report if requested
        report_url = None
        if request.options.get('generate_report', False):
            full_data = {
                **scan_data,
                "scan_id": scan_id,
                "timestamp": timestamp,
                "model_breakdown": fusion_result["model_breakdown"],
                "model_consensus": fusion_result["model_consensus"],
                "confidence_interval": fusion_result["confidence_interval"],
                "calibrated_probability": fusion_result["calibrated_probability"],
                "dynamic_adjustments": fusion_result["dynamic_adjustments"],
                "authentication": email_result.get("authentication") if email_result else None,
                "visual_matches": visual_result.get("visual_matches") if visual_result else None,
                "screenshot_path": screenshot_path
            }
            
            pdf_generator = ForensicReportGenerator()
            report_path = pdf_generator.generate(full_data)
            
            crud.create_report(db, {
                "scan_id": scan_id,
                "file_path": report_path,
                "file_size": 0  # Will be updated
            })
            
            # Update scan record
            crud.update_scan(db, scan_id, {
                "report_generated": True,
                "report_path": report_path
            })
            
            report_url = f"/api/v1/reports/download/{scan_id}"
        
        return ScanResponse(
            scan_id=scan_id,
            timestamp=timestamp,
            scan_type=request.type,
            target=request.target[:200],
            final_score=fusion_result["final_score"],
            classification=fusion_result["classification"],
            confidence_interval=fusion_result["confidence_interval"],
            model_breakdown=fusion_result["model_breakdown"],
            indicators=fusion_result["indicators"],
            mitigation_steps=fusion_result["mitigation_steps"],
            report_url=report_url
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{scan_id}")
async def get_scan(scan_id: str, db: Session = Depends(get_db)):
    """Get scan by ID."""
    scan = crud.get_scan(db, scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    return {
        "scan_id": scan.id,
        "timestamp": scan.timestamp.isoformat(),
        "scan_type": scan.scan_type,
        "target": scan.target,
        "final_score": scan.final_score,
        "classification": scan.classification,
        "indicators": scan.indicators,
        "mitigation_steps": scan.mitigation_steps,
        "impersonated_brand": scan.impersonated_brand,
        "report_generated": scan.report_generated
    }


@router.get("/")
async def list_scans(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List recent scans."""
    scans = crud.get_scans(db, skip=skip, limit=limit)
    
    return {
        "total": len(scans),
        "scans": [
            {
                "scan_id": s.id,
                "timestamp": s.timestamp.isoformat(),
                "scan_type": s.scan_type,
                "final_score": s.final_score,
                "classification": s.classification
            }
            for s in scans
        ]
    }
