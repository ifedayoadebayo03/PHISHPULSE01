"""
Report endpoints for PDF generation and download.
"""

import os
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from backend.database.models import get_db
from backend.database import crud
from backend.services.pdf_generator import ForensicReportGenerator

router = APIRouter()


@router.get("/download/{scan_id}")
async def download_report(scan_id: str, db: Session = Depends(get_db)):
    """
    Download PDF report for a scan.
    
    - **scan_id**: ID of the scan
    """
    scan = crud.get_scan(db, scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    if scan.report_path and os.path.exists(scan.report_path):
        return FileResponse(
            scan.report_path,
            media_type="application/pdf",
            filename=f"phishpulse_report_{scan_id}.pdf"
        )
    
    # Generate report on-demand
    from datetime import datetime
    
    full_data = {
        "scan_id": scan_id,
        "timestamp": scan.timestamp.isoformat(),
        "scan_type": scan.scan_type,
        "target": scan.target,
        "final_score": scan.final_score,
        "classification": scan.classification,
        "confidence_interval": [scan.confidence_lower, scan.confidence_upper],
        "indicators": scan.indicators,
        "mitigation_steps": scan.mitigation_steps,
        "impersonated_brand": scan.impersonated_brand,
        "model_breakdown": {
            "url_analyzer": {"score": scan.url_score, "weight": 0.30},
            "email_forensics": {"score": scan.email_score, "weight": 0.35},
            "visual_detector": {"score": scan.visual_score, "weight": 0.35}
        }
    }
    
    pdf_generator = ForensicReportGenerator()
    report_path = pdf_generator.generate(full_data)
    
    # Update scan record
    crud.update_scan(db, scan_id, {
        "report_generated": True,
        "report_path": report_path
    })
    
    return FileResponse(
        report_path,
        media_type="application/pdf",
        filename=f"phishpulse_report_{scan_id}.pdf"
    )


@router.post("/generate/{scan_id}")
async def generate_report(scan_id: str, db: Session = Depends(get_db)):
    """
    Generate PDF report for a scan.
    
    - **scan_id**: ID of the scan
    """
    scan = crud.get_scan(db, scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    full_data = {
        "scan_id": scan_id,
        "timestamp": scan.timestamp.isoformat(),
        "scan_type": scan.scan_type,
        "target": scan.target,
        "final_score": scan.final_score,
        "classification": scan.classification,
        "confidence_interval": [scan.confidence_lower, scan.confidence_upper],
        "indicators": scan.indicators,
        "mitigation_steps": scan.mitigation_steps,
        "impersonated_brand": scan.impersonated_brand,
        "model_breakdown": {
            "url_analyzer": {"score": scan.url_score, "weight": 0.30},
            "email_forensics": {"score": scan.email_score, "weight": 0.35},
            "visual_detector": {"score": scan.visual_score, "weight": 0.35}
        }
    }
    
    pdf_generator = ForensicReportGenerator()
    report_path = pdf_generator.generate(full_data)
    
    # Update scan record
    crud.update_scan(db, scan_id, {
        "report_generated": True,
        "report_path": report_path
    })
    
    return {
        "scan_id": scan_id,
        "report_path": report_path,
        "message": "Report generated successfully"
    }


@router.get("/")
async def list_reports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List generated reports."""
    from backend.database.models import Report
    
    reports = db.query(Report).offset(skip).limit(limit).all()
    
    return {
        "total": len(reports),
        "reports": [
            {
                "report_id": r.id,
                "scan_id": r.scan_id,
                "created_at": r.created_at.isoformat(),
                "file_path": r.file_path
            }
            for r in reports
        ]
    }
