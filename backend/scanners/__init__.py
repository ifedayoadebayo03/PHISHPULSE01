"""
The Four AI Models of PhishPulse.

Model A: URL Lexical Analyzer (Isolation Forest) - Unsupervised
Model B: Email Forensic Analyzer (Naive Bayes) - Supervised  
Model C: Visual Phishing Detector (ORB + pHash) - Unsupervised
Model D: Risk Fusion Engine (Weighted Ensemble) - Meta-Classifier
"""

from .url_lexical import URLLexicalAnalyzer
from .email_forensics import EmailForensicAnalyzer
from .visual_detector import VisualPhishingDetector
from .risk_fusion import RiskFusionEngine

__all__ = [
    "URLLexicalAnalyzer",
    "EmailForensicAnalyzer", 
    "VisualPhishingDetector",
    "RiskFusionEngine"
]
