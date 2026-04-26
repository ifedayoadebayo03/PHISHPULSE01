"""
API router aggregation for v1 endpoints.
"""

from fastapi import APIRouter

from backend.api.v1.endpoints import scan, report, health

api_router = APIRouter()

api_router.include_router(scan.router, prefix="/scan", tags=["scan"])
api_router.include_router(report.router, prefix="/reports", tags=["reports"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
