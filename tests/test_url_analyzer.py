"""
Unit tests for URL Lexical Analyzer (Model A).
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.scanners.url_lexical import URLLexicalAnalyzer


class TestURLLexicalAnalyzer:
    """Test cases for URL Lexical Analyzer."""
    
    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance."""
        return URLLexicalAnalyzer()
    
    def test_calculate_entropy(self, analyzer):
        """Test Shannon entropy calculation."""
        # High entropy (random)
        high_entropy = analyzer._calculate_entropy("xn--bcher-kva.example")
        assert high_entropy > 3.0
        
        # Low entropy (repetitive)
        low_entropy = analyzer._calculate_entropy("aaaaaa")
        assert low_entropy < 1.0
    
    def test_levenshtein_distance(self, analyzer):
        """Test Levenshtein distance calculation."""
        distance = analyzer._levenshtein_distance("paypa1", "paypal")
        assert distance == 1
        
        distance = analyzer._levenshtein_distance("google", "g00gle")
        assert distance == 2
    
    def test_extract_features(self, analyzer):
        """Test feature extraction."""
        url = "https://www.example.com/path?query=1"
        features = analyzer._extract_features(url)
        
        assert features.shape == (16,)
        assert features[0] >= 0  # entropy
        assert features[14] == 1  # has_https
    
    def test_analyze_safe_url(self, analyzer):
        """Test analysis of safe URL."""
        result = analyzer.analyze("https://www.google.com")
        
        assert "score" in result
        assert "indicators" in result
        assert isinstance(result["score"], int)
        assert 0 <= result["score"] <= 100
    
    def test_analyze_suspicious_url(self, analyzer):
        """Test analysis of suspicious URL."""
        # Typosquatting URL
        result = analyzer.analyze("https://paypa1-security-update.tk/login")
        
        assert result["score"] > 50  # Should be flagged as suspicious
        assert any("typosquatting" in i.lower() or "suspicious" in i.lower() 
                   for i in result["indicators"])
    
    def test_typosquatting_detection(self, analyzer):
        """Test typosquatting detection."""
        candidates = analyzer._get_typosquatting_candidates("paypa1")
        
        assert len(candidates) > 0
        assert any(c["brand"] == "paypal.com" for c in candidates)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
