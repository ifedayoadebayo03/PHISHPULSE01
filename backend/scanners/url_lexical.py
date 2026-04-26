"""
Model A: URL Lexical Analyzer
Unsupervised anomaly detection using Isolation Forest + Regex Heuristics.

Key Innovation: Trained exclusively on benign URLs to detect zero-day phishing
via structural anomaly identification without pre-labeled malicious datasets.
"""

import re
import math
import gzip
import joblib
import numpy as np
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse
from collections import Counter
import Levenshtein
import tldextract

from backend.app.config import settings


class URLLexicalAnalyzer:
    """
    URL Lexical Analyzer using Isolation Forest for unsupervised anomaly detection.
    
    Features:
    - Shannon Entropy (DGA detection)
    - Levenshtein Distance (typosquatting detection)
    - Suspicious TLD scoring
    - Subdomain depth analysis
    - URL length and structure analysis
    """
    
    # Suspicious keywords commonly found in phishing URLs
    SUSPICIOUS_KEYWORDS = [
        "login", "signin", "verify", "secure", "account", "update",
        "confirm", "validation", "authenticate", "password", "credential",
        "banking", "wallet", "payment", "billing", "invoice", "security",
        "suspend", "locked", "unusual", "activity", "verify-account",
        "sign-in", "log-in", "update-info", "confirm-identity"
    ]
    
    # Brand domains for Levenshtein comparison
    TOP_BRANDS = [
        "paypal.com", "microsoft.com", "apple.com", "google.com",
        "amazon.com", "facebook.com", "netflix.com", "bankofamerica.com",
        "chase.com", "wellsfargo.com", "citibank.com", "americanexpress.com",
        "linkedin.com", "twitter.com", "instagram.com", "dropbox.com",
        "adobe.com", "office.com", "onedrive.com", "icloud.com"
    ]
    
    def __init__(self, model_path: Optional[str] = None):
        """Initialize URL analyzer with optional pre-trained model."""
        self.model = None
        self.model_path = model_path or settings.URL_MODEL_PATH
        self.is_fitted = False
        
        # Feature names for interpretability
        self.feature_names = [
            "entropy", "url_length", "path_length", "query_param_count",
            "subdomain_depth", "has_ip_address", "has_at_symbol",
            "has_double_slash", "dash_count", "dot_count", "digit_count",
            "suspicious_keyword_count", "tld_risk", "levenshtein_min",
            "has_https", "special_char_ratio"
        ]
        
        self._load_model()
    
    def _load_model(self):
        """Load pre-trained Isolation Forest model."""
        try:
            if self.model_path.endswith('.gz'):
                with gzip.open(self.model_path, 'rb') as f:
                    self.model = joblib.load(f)
            else:
                self.model = joblib.load(self.model_path)
            self.is_fitted = True
        except FileNotFoundError:
            # Initialize new model (will need training)
            from sklearn.ensemble import IsolationForest
            self.model = IsolationForest(
                contamination=settings.URL_CONTAMINATION,
                n_estimators=settings.URL_N_ESTIMATORS,
                max_samples=settings.URL_MAX_SAMPLES,
                random_state=42,
                n_jobs=-1
            )
            self.is_fitted = False
    
    def _calculate_entropy(self, string: str) -> float:
        """Calculate Shannon entropy of a string (DGA detection)."""
        if not string:
            return 0.0
        
        # Calculate character frequency
        char_counts = Counter(string)
        length = len(string)
        
        # Shannon entropy formula: H(X) = -sum(p(x) * log2(p(x)))
        entropy = -sum(
            (count / length) * math.log2(count / length)
            for count in char_counts.values()
        )
        return round(entropy, 4)
    
    def _levenshtein_distance(self, domain: str, target: str) -> int:
        """Calculate Levenshtein distance between domain and target."""
        return Levenshtein.distance(domain.lower(), target.lower())
    
    def _extract_features(self, url: str) -> np.ndarray:
        """
        Extract 16 numerical features from URL for anomaly detection.
        
        Returns:
            numpy array of shape (16,)
        """
        try:
            parsed = urlparse(url)
            extracted = tldextract.extract(url)
        except Exception:
            return np.zeros(16)
        
        domain = f"{extracted.domain}.{extracted.suffix}" if extracted.suffix else extracted.domain
        full_domain = f"{extracted.subdomain}.{domain}" if extracted.subdomain else domain
        
        # 1. Shannon entropy of domain
        entropy = self._calculate_entropy(domain)
        
        # 2-3. URL and path length
        url_length = len(url)
        path_length = len(parsed.path)
        
        # 4. Query parameter count
        query_param_count = len(parsed.query.split('&')) if parsed.query else 0
        
        # 5. Subdomain depth
        subdomain_depth = len(extracted.subdomain.split('.')) if extracted.subdomain else 0
        
        # 6. Has IP address
        has_ip = bool(re.match(
            r'^(\d{1,3}\.){3}\d{1,3}$', 
            extracted.domain
        ))
        
        # 7. Has @ symbol (credential leakage attempt)
        has_at = '@' in url
        
        # 8. Has double slash in path (redirect abuse)
        has_double_slash = '//' in parsed.path
        
        # 9-11. Character counts
        dash_count = url.count('-')
        dot_count = url.count('.')
        digit_count = sum(c.isdigit() for c in url)
        
        # 12. Suspicious keyword count
        url_lower = url.lower()
        suspicious_keyword_count = sum(
            1 for kw in self.SUSPICIOUS_KEYWORDS if kw in url_lower
        )
        
        # 13. TLD risk score
        tld = f".{extracted.suffix}" if extracted.suffix else ""
        tld_risk = settings.SUSPICIOUS_TLDS.get(tld, 0)
        
        # 14. Minimum Levenshtein distance to top brands
        domain_without_tld = extracted.domain.lower()
        levenshtein_min = min(
            self._levenshtein_distance(domain_without_tld, brand.split('.')[0])
            for brand in self.TOP_BRANDS
        ) if self.TOP_BRANDS else 99
        
        # 15. Has HTTPS
        has_https = parsed.scheme == 'https'
        
        # 16. Special character ratio
        special_chars = sum(1 for c in url if not c.isalnum())
        special_char_ratio = special_chars / len(url) if url else 0
        
        features = np.array([
            entropy,
            min(url_length, 500) / 500,  # Normalize
            min(path_length, 200) / 200,
            min(query_param_count, 10) / 10,
            min(subdomain_depth, 5) / 5,
            float(has_ip),
            float(has_at),
            float(has_double_slash),
            min(dash_count, 10) / 10,
            min(dot_count, 10) / 10,
            min(digit_count, 20) / 20,
            min(suspicious_keyword_count, 5) / 5,
            min(tld_risk, 20) / 20,
            min(levenshtein_min, 10) / 10,
            float(has_https),
            special_char_ratio
        ])
        
        return features
    
    def _get_typosquatting_candidates(self, domain: str) -> List[str]:
        """Identify potential typosquatting candidates."""
        candidates = []
        domain_lower = domain.lower()
        
        for brand in self.TOP_BRANDS:
            brand_domain = brand.split('.')[0]
            distance = self._levenshtein_distance(domain_lower, brand_domain)
            
            # Flag if distance is small but not exact match (likely typosquatting)
            if 0 < distance <= 2:
                candidates.append({
                    "brand": brand,
                    "distance": distance,
                    "type": self._classify_typosquatting(domain_lower, brand_domain)
                })
        
        return candidates
    
    def _classify_typosquatting(self, domain: str, brand: str) -> str:
        """Classify type of typosquatting attack."""
        # Character substitution (o -> 0, l -> 1, etc.)
        substitutions = {'o': '0', 'l': '1', 'i': '1', 's': '5', 'g': '9', 'q': '9'}
        domain_sub = ''.join(substitutions.get(c, c) for c in domain)
        brand_sub = ''.join(substitutions.get(c, c) for c in brand)
        if domain_sub == brand_sub:
            return "character_substitution"
        
        # Character omission
        if any(Levenshtein.distance(domain, brand.replace(c, '')) == 0 for c in brand):
            return "character_omission"
        
        # Character addition
        if any(Levenshtein.distance(domain.replace(c, ''), brand) == 0 for c in domain):
            return "character_addition"
        
        # Character swap (adjacent transposition)
        for i in range(len(domain) - 1):
            swapped = domain[:i] + domain[i+1] + domain[i] + domain[i+2:]
            if swapped == brand:
                return "character_swap"
        
        return "homograph_or_other"
    
    def analyze(self, url: str) -> Dict:
        """
        Analyze URL for phishing indicators.
        
        Returns:
            Dict with risk score, indicators, and anomalies
        """
        # Extract features
        features = self._extract_features(url)
        
        # Parse URL components
        try:
            extracted = tldextract.extract(url)
            domain = f"{extracted.domain}.{extracted.suffix}" if extracted.suffix else extracted.domain
        except Exception:
            domain = url
            extracted = None
        
        # Calculate individual risk components
        indicators = []
        
        # Entropy check (DGA detection)
        entropy = features[0]
        if entropy > 4.0:
            indicators.append(f"High entropy domain detected ({entropy:.2f}) - possible DGA")
        
        # Typosquatting detection
        typosquatting = self._get_typosquatting_candidates(extracted.domain if extracted else "")
        if typosquatting:
            best_match = min(typosquatting, key=lambda x: x['distance'])
            indicators.append(
                f"Possible typosquatting of {best_match['brand']} "
                f"(distance: {best_match['distance']}, type: {best_match['type']})"
            )
        
        # Suspicious TLD
        if extracted:
            tld = f".{extracted.suffix}" if extracted.suffix else ""
            if tld in settings.SUSPICIOUS_TLDS:
                indicators.append(f"Suspicious TLD detected: {tld} (risk: +{settings.SUSPICIOUS_TLDS[tld]})")
        
        # Subdomain depth
        subdomain_depth = features[4] * 5  # Denormalize
        if subdomain_depth >= 3:
            indicators.append(f"Excessive subdomain nesting (depth: {int(subdomain_depth)})")
        
        # IP address in URL
        if features[5] == 1:
            indicators.append("IP address used instead of domain name")
        
        # @ symbol (credential phishing)
        if features[6] == 1:
            indicators.append("URL contains @ symbol (credential obfuscation)")
        
        # Suspicious keywords
        keyword_count = int(features[11] * 5)
        if keyword_count > 0:
            indicators.append(f"Contains {keyword_count} suspicious keyword(s)")
        
        # No HTTPS
        if features[14] == 0:
            indicators.append("No HTTPS encryption")
        
        # Calculate anomaly score using Isolation Forest if available
        if self.is_fitted and self.model:
            # Isolation Forest: -1 for anomaly, 1 for normal
            # Convert to 0-100 risk score
            anomaly_score = self.model.decision_function([features])[0]
            # anomaly_score ranges from -0.5 to 0.5 typically
            # Normalize to 0-100
            base_score = int((0.5 - anomaly_score) * 100)
        else:
            # Heuristic fallback when model not trained
            base_score = self._heuristic_score(features)
        
        # Clamp score to 0-100
        risk_score = max(0, min(100, base_score))
        
        # Determine impersonated brand
        impersonated_brand = None
        if typosquatting:
            impersonated_brand = min(typosquatting, key=lambda x: x['distance'])['brand']
        
        return {
            "score": risk_score,
            "confidence": round(0.7 + (abs(50 - risk_score) / 100), 2),  # Higher confidence at extremes
            "indicators": indicators,
            "impersonated_brand": impersonated_brand,
            "structural_anomalies": self._get_anomaly_descriptions(features),
            "feature_vector": features.tolist()
        }
    
    def _heuristic_score(self, features: np.ndarray) -> int:
        """Calculate heuristic score when model not available."""
        score = 0
        
        # High entropy
        if features[0] > 3.5:
            score += 20
        
        # Very long URL
        if features[1] > 0.8:
            score += 10
        
        # Deep subdomain
        if features[4] > 0.6:
            score += 15
        
        # IP address
        if features[5] == 1:
            score += 25
        
        # @ symbol
        if features[6] == 1:
            score += 20
        
        # Suspicious keywords
        score += features[11] * 20
        
        # TLD risk
        score += features[12] * 20
        
        # Typosquatting
        if features[13] < 0.3:  # Low Levenshtein distance
            score += 25
        
        # No HTTPS
        if features[14] == 0:
            score += 10
        
        return min(100, score)
    
    def _get_anomaly_descriptions(self, features: np.ndarray) -> List[str]:
        """Get human-readable descriptions of structural anomalies."""
        anomalies = []
        
        if features[0] > 3.5:
            anomalies.append("high_entropy")
        if features[4] > 0.4:
            anomalies.append("deep_subdomain_nesting")
        if features[5] == 1:
            anomalies.append("ip_address_in_url")
        if features[6] == 1:
            anomalies.append("at_symbol_present")
        if features[7] == 1:
            anomalies.append("double_slash_in_path")
        if features[13] < 0.3:
            anomalies.append("similar_to_known_brand")
        
        return anomalies
    
    def train(self, benign_urls: List[str]):
        """
        Train Isolation Forest on benign URLs only (unsupervised).
        
        Args:
            benign_urls: List of known benign URLs
        """
        print(f"Training URL Lexical Analyzer on {len(benign_urls)} benign URLs...")
        
        # Extract features for all URLs
        X = np.array([self._extract_features(url) for url in benign_urls])
        
        # Train Isolation Forest
        self.model.fit(X)
        self.is_fitted = True
        
        # Save model
        self._save_model()
        
        print(f"Training complete. Model saved to {self.model_path}")
    
    def _save_model(self):
        """Save model to disk with compression."""
        import os
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        
        if self.model_path.endswith('.gz'):
            with gzip.open(self.model_path, 'wb', compresslevel=3) as f:
                joblib.dump(self.model, f)
        else:
            joblib.dump(self.model, self.model_path, compress=3)
    
    def partial_train(self, batch_urls: List[str]):
        """
        Incremental training with warm_start (memory efficient).
        
        Note: Isolation Forest doesn't support true partial fit,
        but we can simulate with warm_start by incrementing estimators.
        """
        if not self.is_fitted:
            raise ValueError("Model must be initially trained before partial updates")
        
        X_batch = np.array([self._extract_features(url) for url in batch_urls])
        
        # Update model with warm_start
        if hasattr(self.model, 'warm_start'):
            self.model.warm_start = True
            current_estimators = self.model.n_estimators
            self.model.n_estimators = current_estimators + 10
            self.model.fit(X_batch)
        
        self._save_model()
