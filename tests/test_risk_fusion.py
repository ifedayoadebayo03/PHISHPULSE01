"""
Unit tests for Risk Fusion Engine (Model D).
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.scanners.risk_fusion import RiskFusionEngine, ModelResult


class TestRiskFusionEngine:
    """Test cases for Risk Fusion Engine."""
    
    @pytest.fixture
    def engine(self):
        """Create fusion engine instance."""
        return RiskFusionEngine()
    
    def test_fuse_all_models(self, engine):
        """Test fusion with all models."""
        url_result = {"score": 70, "confidence": 0.8, "indicators": []}
        email_result = {"score": 60, "confidence": 0.75, "indicators": []}
        visual_result = {"score": 80, "confidence": 0.85, "indicators": []}
        
        result = engine.fuse(
            url_result=url_result,
            email_result=email_result,
            visual_result=visual_result
        )
        
        assert "final_score" in result
        assert "classification" in result
        assert 0 <= result["final_score"] <= 100
    
    def test_fuse_partial_models(self, engine):
        """Test fusion with only URL model."""
        url_result = {"score": 90, "confidence": 0.8, "indicators": ["suspicious"]}
        
        result = engine.fuse(url_result=url_result)
        
        assert result["final_score"] > 0
        assert result["classification"] in ["Clean", "Suspicious", "Malicious", "Critical"]
    
    def test_dynamic_adjustments(self, engine):
        """Test domain age and SSL penalties."""
        url_result = {"score": 50, "confidence": 0.8, "indicators": []}
        
        result = engine.fuse(
            url_result=url_result,
            domain_age_days=3,  # Very new domain
            has_valid_ssl=False
        )
        
        # Should have penalties applied
        assert result["final_score"] > 50
        assert result["dynamic_adjustments"]["domain_age_penalty"] > 0
        assert result["dynamic_adjustments"]["ssl_penalty"] > 0
    
    def test_classification_thresholds(self, engine):
        """Test classification based on score thresholds."""
        test_cases = [
            (20, "Clean"),
            (45, "Suspicious"),
            (75, "Malicious"),
            (95, "Critical")
        ]
        
        for score, expected_class in test_cases:
            url_result = {"score": score, "confidence": 0.8, "indicators": []}
            result = engine.fuse(url_result=url_result)
            assert result["classification"] == expected_class
    
    def test_model_consensus(self, engine):
        """Test model consensus calculation."""
        model_results = [
            ModelResult("URL", 80, 0.3, 0.8, []),
            ModelResult("Email", 85, 0.35, 0.85, []),
            ModelResult("Visual", 90, 0.35, 0.9, [])
        ]
        
        consensus = engine._get_model_consensus(model_results)
        
        assert consensus["models_contributing"] == 3
        assert len(consensus["votes"]) == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
