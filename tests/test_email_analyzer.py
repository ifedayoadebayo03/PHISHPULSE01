"""
Unit tests for Email Forensic Analyzer (Model B).
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.scanners.email_forensics import EmailForensicAnalyzer, EmailHeaders


class TestEmailForensicAnalyzer:
    """Test cases for Email Forensic Analyzer."""
    
    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance."""
        return EmailForensicAnalyzer()
    
    def test_extract_headers(self, analyzer):
        """Test header extraction."""
        raw_email = """From: sender@example.com
To: recipient@example.com
Subject: Test Email
Return-Path: <bounce@example.com>
Authentication-Results: spf=pass; dkim=pass; dmarc=pass

Body content here."""
        
        headers = analyzer._extract_headers(raw_email)
        
        assert headers.from_address == "sender@example.com"
        assert headers.from_domain == "example.com"
        assert headers.return_path == "bounce@example.com"
    
    def test_calculate_urgency_score(self, analyzer):
        """Test urgency keyword detection."""
        text = "URGENT: Verify your account immediately or it will be suspended!"
        score = analyzer._calculate_urgency_score(text)
        
        assert score > 0
    
    def test_calculate_html_text_ratio(self, analyzer):
        """Test HTML ratio calculation."""
        html_text = "<html><body><p>Hello</p></body></html>"
        ratio = analyzer._calculate_html_text_ratio(html_text)
        
        assert ratio > 0
    
    def test_check_authentication_alignment(self, analyzer):
        """Test authentication checks."""
        headers = EmailHeaders(
            from_address="user@example.com",
            from_domain="example.com",
            return_path="bounce@example.com",
            return_path_domain="example.com",
            spf_result="pass",
            dkim_result="pass",
            dmarc_result="pass",
            received_chain=[]
        )
        
        checks = analyzer._check_authentication_alignment(headers)
        
        assert checks["spf_aligned"] is True
        assert checks["dkim_aligned"] is True
        assert checks["return_path_match"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
