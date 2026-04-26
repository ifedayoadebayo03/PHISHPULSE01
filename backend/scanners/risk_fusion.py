"""
Model D: Risk Fusion Engine
Meta-classifier ensemble using weighted voting + isotonic regression.

Purpose: Multi-modal signal aggregation with calibrated confidence intervals.
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from sklearn.isotonic import IsotonicRegression
import joblib
from datetime import datetime

from backend.app.config import settings


@dataclass
class ModelResult:
    """Individual model result."""
    model_name: str
    score: int
    weight: float
    confidence: float
    indicators: List[str]


class RiskFusionEngine:
    """
    Risk Fusion Engine for combining multi-modal signals.
    
    Weights:
    - URL Analysis: 30%
    - Email Forensics: 35%
    - Visual Detection: 35%
    
    Thresholds:
    - 0-30: Clean (Green)
    - 31-60: Suspicious (Amber)
    - 61-85: Malicious (Red)
    - 86-100: Critical (Crimson)
    """
    
    # Risk classification thresholds
    CLASSIFICATIONS = {
        (0, 30): "Clean",
        (31, 60): "Suspicious",
        (61, 85): "Malicious",
        (86, 100): "Critical"
    }
    
    # Mitigation steps by classification
    MITIGATION_STEPS = {
        "Clean": [
            "No immediate action required",
            "Continue normal monitoring",
            "Report false positive if incorrect"
        ],
        "Suspicious": [
            "Review source carefully before proceeding",
            "Verify sender through alternative channel",
            "Check URL carefully for typosquatting",
            "Do not enter credentials without verification"
        ],
        "Malicious": [
            "Do not interact with content",
            "Block domain at firewall/proxy",
            "Alert security team",
            "Check for related IOCs in environment",
            "Submit to threat intelligence feeds"
        ],
        "Critical": [
            "BLOCK DOMAIN IMMEDIATELY",
            "Isolate any affected endpoints",
            "Reset credentials if potentially compromised",
            "Initiate incident response procedure",
            "Submit to PhishTank and other threat feeds",
            "Notify affected users immediately",
            "Preserve logs for forensic analysis"
        ]
    }
    
    def __init__(self, calibration_model_path: Optional[str] = None):
        """Initialize risk fusion engine."""
        self.calibration_model = None
        self.calibration_model_path = calibration_model_path or "models/risk_calibration.pkl"
        
        # Weights from settings
        self.url_weight = settings.URL_WEIGHT
        self.email_weight = settings.EMAIL_WEIGHT
        self.visual_weight = settings.VISUAL_WEIGHT
        
        self._load_calibration()
    
    def _load_calibration(self):
        """Load isotonic regression calibration model."""
        try:
            self.calibration_model = joblib.load(self.calibration_model_path)
        except FileNotFoundError:
            # Will be trained on first use
            self.calibration_model = None
    
    def _calculate_weighted_score(
        self,
        url_score: Optional[int],
        email_score: Optional[int],
        visual_score: Optional[int]
    ) -> float:
        """Calculate weighted ensemble score."""
        weighted_sum = 0.0
        total_weight = 0.0
        
        if url_score is not None:
            weighted_sum += url_score * self.url_weight
            total_weight += self.url_weight
        
        if email_score is not None:
            weighted_sum += email_score * self.email_weight
            total_weight += self.email_weight
        
        if visual_score is not None:
            weighted_sum += visual_score * self.visual_weight
            total_weight += self.visual_weight
        
        if total_weight == 0:
            return 0.0
        
        return weighted_sum / total_weight
    
    def _apply_dynamic_adjustments(
        self,
        base_score: float,
        domain_age_days: Optional[int],
        has_valid_ssl: Optional[bool]
    ) -> float:
        """Apply dynamic risk adjustments."""
        adjusted_score = base_score
        
        # Domain age penalty
        if domain_age_days is not None and domain_age_days < settings.DOMAIN_AGE_DAYS:
            adjusted_score += settings.DOMAIN_AGE_PENALTY
        
        # SSL invalid penalty
        if has_valid_ssl is False:
            adjusted_score += settings.SSL_INVALID_PENALTY
        
        return min(100, adjusted_score)
    
    def _get_classification(self, score: int) -> str:
        """Get classification label for score."""
        for (min_score, max_score), label in self.CLASSIFICATIONS.items():
            if min_score <= score <= max_score:
                return label
        return "Unknown"
    
    def _calculate_confidence_interval(
        self,
        model_results: List[ModelResult],
        final_score: int
    ) -> Tuple[float, float]:
        """Calculate 95% confidence interval using model variance."""
        if not model_results:
            return (0.0, 1.0)
        
        # Calculate variance in model scores
        scores = [r.score for r in model_results]
        if len(scores) < 2:
            return (max(0, final_score/100 - 0.1), min(1, final_score/100 + 0.1))
        
        variance = np.var(scores)
        std_dev = np.sqrt(variance)
        
        # Convert final score to probability
        base_prob = final_score / 100.0
        
        # 95% CI using normal approximation
        margin = 1.96 * std_dev / 100  # Scale to probability
        
        lower = max(0.0, base_prob - margin)
        upper = min(1.0, base_prob + margin)
        
        return (round(lower, 2), round(upper, 2))
    
    def _calibrate_probability(self, score: int) -> float:
        """Apply isotonic regression calibration if available."""
        if self.calibration_model is None:
            # Simple sigmoid calibration fallback
            return 1 / (1 + np.exp(-0.1 * (score - 50)))
        
        return self.calibration_model.predict([[score]])[0]
    
    def _get_model_consensus(self, model_results: List[ModelResult]) -> Dict:
        """Get voting breakdown from all models."""
        consensus = {
            "models_contributing": len(model_results),
            "agreement_level": "high",
            "votes": []
        }
        
        if not model_results:
            return consensus
        
        # Classify each model's score
        votes = []
        for result in model_results:
            classification = self._get_classification(result.score)
            votes.append({
                "model": result.model_name,
                "score": result.score,
                "weight": result.weight,
                "vote": classification
            })
        
        consensus["votes"] = votes
        
        # Calculate agreement
        classifications = [v["vote"] for v in votes]
        unique_classes = set(classifications)
        
        if len(unique_classes) == 1:
            consensus["agreement_level"] = "unanimous"
        elif len(unique_classes) == 2:
            consensus["agreement_level"] = "partial"
        else:
            consensus["agreement_level"] = "low"
        
        return consensus
    
    def fuse(
        self,
        url_result: Optional[Dict] = None,
        email_result: Optional[Dict] = None,
        visual_result: Optional[Dict] = None,
        domain_age_days: Optional[int] = None,
        has_valid_ssl: Optional[bool] = None
    ) -> Dict:
        """
        Fuse multi-modal results into final risk assessment.
        
        Args:
            url_result: Result from URL Lexical Analyzer
            email_result: Result from Email Forensic Analyzer
            visual_result: Result from Visual Phishing Detector
            domain_age_days: Optional domain age in days
            has_valid_ssl: Optional SSL validity flag
        
        Returns:
            Dict with final verdict, confidence intervals, and mitigation steps
        """
        # Extract scores
        url_score = url_result.get("score") if url_result else None
        email_score = email_result.get("score") if email_result else None
        visual_score = visual_result.get("score") if visual_result else None
        
        # Create model results list
        model_results = []
        if url_result:
            model_results.append(ModelResult(
                model_name="URL Lexical Analyzer",
                score=url_score,
                weight=self.url_weight,
                confidence=url_result.get("confidence", 0.5),
                indicators=url_result.get("indicators", [])
            ))
        if email_result:
            model_results.append(ModelResult(
                model_name="Email Forensic Analyzer",
                score=email_score,
                weight=self.email_weight,
                confidence=email_result.get("confidence", 0.5),
                indicators=email_result.get("indicators", [])
            ))
        if visual_result:
            model_results.append(ModelResult(
                model_name="Visual Phishing Detector",
                score=visual_score,
                weight=self.visual_weight,
                confidence=visual_result.get("confidence", 0.5),
                indicators=visual_result.get("indicators", [])
            ))
        
        # Calculate weighted score
        weighted_score = self._calculate_weighted_score(
            url_score, email_score, visual_score
        )
        
        # Apply dynamic adjustments
        adjusted_score = self._apply_dynamic_adjustments(
            weighted_score, domain_age_days, has_valid_ssl
        )
        
        # Clamp to 0-100
        final_score = int(round(max(0, min(100, adjusted_score))))
        
        # Get classification
        classification = self._get_classification(final_score)
        
        # Calculate confidence interval
        ci_lower, ci_upper = self._calculate_confidence_interval(model_results, final_score)
        
        # Get model consensus
        consensus = self._get_model_consensus(model_results)
        
        # Aggregate indicators
        all_indicators = []
        for result in model_results:
            all_indicators.extend(result.indicators)
        
        # Add dynamic adjustment indicators
        if domain_age_days is not None and domain_age_days < settings.DOMAIN_AGE_DAYS:
            all_indicators.append(
                f"Domain registered recently ({domain_age_days} days ago)"
            )
        if has_valid_ssl is False:
            all_indicators.append("Invalid or missing SSL certificate")
        
        # Deduplicate indicators
        unique_indicators = list(dict.fromkeys(all_indicators))
        
        # Get mitigation steps
        mitigation = self.MITIGATION_STEPS.get(classification, [])
        
        # Identify impersonated brand
        impersonated_brand = None
        if url_result and url_result.get("impersonated_brand"):
            impersonated_brand = url_result["impersonated_brand"]
        elif visual_result and visual_result.get("impersonated_brand"):
            impersonated_brand = visual_result["impersonated_brand"]
        
        return {
            "final_score": final_score,
            "classification": classification,
            "confidence_interval": [ci_lower, ci_upper],
            "model_breakdown": {
                "url_analyzer": {
                    "score": url_score,
                    "weight": self.url_weight,
                    "contribution": round((url_score or 0) * self.url_weight, 2)
                },
                "email_forensics": {
                    "score": email_score,
                    "weight": self.email_weight,
                    "contribution": round((email_score or 0) * self.email_weight, 2)
                },
                "visual_detector": {
                    "score": visual_score,
                    "weight": self.visual_weight,
                    "contribution": round((visual_score or 0) * self.visual_weight, 2)
                }
            },
            "model_consensus": consensus,
            "indicators": unique_indicators,
            "mitigation_steps": mitigation,
            "impersonated_brand": impersonated_brand,
            "dynamic_adjustments": {
                "domain_age_penalty": settings.DOMAIN_AGE_PENALTY if (domain_age_days is not None and domain_age_days < settings.DOMAIN_AGE_DAYS) else 0,
                "ssl_penalty": settings.SSL_INVALID_PENALTY if has_valid_ssl is False else 0
            },
            "calibrated_probability": round(self._calibrate_probability(final_score), 4)
        }
    
    def calibrate(self, scores: List[int], true_labels: List[int]):
        """
        Train isotonic regression calibration model.
        
        Args:
            scores: List of raw risk scores
            true_labels: List of true labels (0 = benign, 1 = phishing)
        """
        from sklearn.isotonic import IsotonicRegression
        
        # Convert to probabilities
        X = np.array(scores).reshape(-1, 1)
        y = np.array(true_labels)
        
        # Train isotonic regression
        self.calibration_model = IsotonicRegression(y_min=0, y_max=1, out_of_bounds='clip')
        self.calibration_model.fit(X.ravel(), y)
        
        # Save model
        import os
        os.makedirs(os.path.dirname(self.calibration_model_path), exist_ok=True)
        joblib.dump(self.calibration_model, self.calibration_model_path)
        
        print(f"Calibration model saved to {self.calibration_model_path}")
    
    def get_feature_importance(self) -> Dict:
        """Get feature importance (model weights)."""
        return {
            "url_lexical_analyzer": {
                "weight": self.url_weight,
                "description": "Isolation Forest + Regex Heuristics"
            },
            "email_forensic_analyzer": {
                "weight": self.email_weight,
                "description": "TF-IDF + Naive Bayes + Header Analysis"
            },
            "visual_phishing_detector": {
                "weight": self.visual_weight,
                "description": "ORB + Perceptual Hashing"
            }
        }
