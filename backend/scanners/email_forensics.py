"""
Model B: Email Forensic Analyzer
Supervised classification using TF-IDF + Multinomial Naive Bayes + Header Heuristics.

Purpose: Authentication protocol validation and semantic content analysis.
"""

import re
import dns.resolver
import hashlib
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from email.utils import parseaddr
import numpy as np

from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

from backend.app.config import settings


@dataclass
class EmailHeaders:
    """Parsed email headers."""
    from_address: str
    from_domain: str
    return_path: Optional[str]
    return_path_domain: Optional[str]
    spf_result: Optional[str]
    dkim_result: Optional[str]
    dmarc_result: Optional[str]
    received_chain: List[str]


class EmailForensicAnalyzer:
    """
    Email Forensic Analyzer using Naive Bayes for supervised classification.
    
    Features:
    - SPF/DKIM/DMARC validation
    - Return-Path vs From header analysis
    - TF-IDF semantic analysis
    - Urgency keyword detection
    - HTML-to-text ratio analysis
    """
    
    # HTML tags for ratio calculation
    HTML_TAGS = re.compile(r'<[^>]+>')
    
    # Suspicious sender patterns
    SUSPICIOUS_SENDER_PATTERNS = [
        r'noreply@.*',
        r'support@.*',
        r'security@.*',
        r'admin@.*',
        r'helpdesk@.*',
        r'update@.*',
        r'verify@.*',
        r'confirm@.*',
    ]
    
    def __init__(self, model_path: Optional[str] = None):
        """Initialize email analyzer with optional pre-trained model."""
        self.model_path = model_path or settings.EMAIL_MODEL_PATH
        self.vectorizer = None
        self.model = None
        self.is_fitted = False
        
        self._load_model()
    
    def _load_model(self):
        """Load pre-trained Naive Bayes model and vectorizer."""
        try:
            saved = joblib.load(self.model_path)
            self.model = saved['model']
            # HashingVectorizer is stateless, just recreate
            self.vectorizer = HashingVectorizer(
                n_features=settings.EMAIL_VECTORIZER_FEATURES,
                alternate_sign=False
            )
            self.is_fitted = True
        except FileNotFoundError:
            # Initialize new model
            self.vectorizer = HashingVectorizer(
                n_features=settings.EMAIL_VECTORIZER_FEATURES,
                alternate_sign=False
            )
            self.model = MultinomialNB()
            self.is_fitted = False
    
    def _extract_headers(self, raw_email: str) -> EmailHeaders:
        """Extract and parse email headers."""
        headers = {}
        
        # Simple header parsing (works for both raw and formatted)
        lines = raw_email.split('\n')
        current_key = None
        
        for line in lines:
            if not line.strip():
                break  # End of headers
            
            if line[0].isspace() and current_key:
                # Continuation of previous header
                headers[current_key] += ' ' + line.strip()
            elif ':' in line:
                key, value = line.split(':', 1)
                current_key = key.strip().lower()
                headers[current_key] = value.strip()
        
        # Parse From address
        from_header = headers.get('from', '')
        from_address = parseaddr(from_header)[1]
        from_domain = from_address.split('@')[1] if '@' in from_address else ''
        
        # Parse Return-Path
        return_path = headers.get('return-path', '')
        return_path = parseaddr(return_path)[1] if return_path else None
        return_path_domain = return_path.split('@')[1] if return_path and '@' in return_path else None
        
        # Authentication results
        auth_results = headers.get('authentication-results', '')
        
        return EmailHeaders(
            from_address=from_address,
            from_domain=from_domain,
            return_path=return_path,
            return_path_domain=return_path_domain,
            spf_result=self._parse_auth_result(auth_results, 'spf'),
            dkim_result=self._parse_auth_result(auth_results, 'dkim'),
            dmarc_result=self._parse_auth_result(auth_results, 'dmarc'),
            received_chain=self._parse_received_chain(headers)
        )
    
    def _parse_auth_result(self, auth_results: str, mechanism: str) -> Optional[str]:
        """Parse SPF/DKIM/DMARC result from Authentication-Results header."""
        pattern = rf'{mechanism}=([^\s;]+)'
        match = re.search(pattern, auth_results, re.IGNORECASE)
        return match.group(1).lower() if match else None
    
    def _parse_received_chain(self, headers: Dict) -> List[str]:
        """Parse Received header chain."""
        received = []
        for key, value in headers.items():
            if key == 'received':
                received.append(value)
        return received
    
    def _check_dns_records(self, domain: str) -> Dict:
        """Check DNS records for authentication alignment."""
        results = {
            'has_spf': False,
            'has_dkim': False,
            'has_dmarc': False,
            'dmarc_policy': None
        }
        
        try:
            # Check SPF
            try:
                answers = dns.resolver.resolve(domain, 'TXT')
                for rdata in answers:
                    txt = str(rdata)
                    if 'v=spf1' in txt:
                        results['has_spf'] = True
                        break
            except dns.resolver.NXDOMAIN:
                pass
            except dns.resolver.NoAnswer:
                pass
            
            # Check DMARC
            try:
                answers = dns.resolver.resolve(f'_dmarc.{domain}', 'TXT')
                for rdata in answers:
                    txt = str(rdata)
                    if 'v=DMARC1' in txt:
                        results['has_dmarc'] = True
                        # Extract policy
                        policy_match = re.search(r'p=([^;\s]+)', txt)
                        if policy_match:
                            results['dmarc_policy'] = policy_match.group(1)
                        break
            except dns.resolver.NXDOMAIN:
                pass
            except dns.resolver.NoAnswer:
                pass
            
        except Exception:
            pass
        
        return results
    
    def _calculate_urgency_score(self, text: str) -> float:
        """Calculate urgency keyword density."""
        text_lower = text.lower()
        words = text_lower.split()
        
        if not words:
            return 0.0
        
        urgency_count = sum(
            1 for keyword in settings.URGENCY_KEYWORDS
            if keyword in text_lower
        )
        
        return round(urgency_count / len(words) * 100, 4)
    
    def _calculate_html_text_ratio(self, text: str) -> float:
        """Calculate HTML-to-text ratio (obfuscation detection)."""
        html_chars = len(self.HTML_TAGS.findall(text))
        total_chars = len(text)
        
        if total_chars == 0:
            return 0.0
        
        return round(html_chars / total_chars, 4)
    
    def _extract_links(self, text: str) -> List[Dict]:
        """Extract and analyze links from email."""
        url_pattern = r'href=["\'](https?://[^"\']+)["\']'
        urls = re.findall(url_pattern, text)
        
        links = []
        for url in urls:
            # Check for href/text mismatch (punycode attack)
            visible_text = re.search(rf'<a[^>]*href=["\']{re.escape(url)}["\'][^>]*>([^<]+)</a>', text)
            visible = visible_text.group(1) if visible_text else ""
            
            links.append({
                'url': url,
                'visible_text': visible,
                'mismatch': url not in visible and visible not in url
            })
        
        return links
    
    def _extract_features(self, email_content: str, headers: EmailHeaders) -> np.ndarray:
        """
        Extract features for Naive Bayes classification.
        
        Returns text features vectorized with HashingVectorizer.
        """
        # Combine subject, body, and normalized headers for analysis
        text_parts = []
        
        # Add body text (strip HTML)
        body_text = self.HTML_TAGS.sub(' ', email_content)
        text_parts.append(body_text)
        
        # Vectorize
        X = self.vectorizer.transform([' '.join(text_parts)])
        
        return X
    
    def _check_authentication_alignment(self, headers: EmailHeaders) -> Dict:
        """Check SPF/DKIM/DMARC alignment."""
        checks = {
            'spf_aligned': headers.spf_result in ['pass', 'neutral'],
            'dkim_aligned': headers.dkim_result in ['pass', 'neutral'],
            'dmarc_aligned': headers.dmarc_result in ['pass', 'neutral'],
            'return_path_match': False,
            'authentication_issues': []
        }
        
        # Return-Path alignment
        if headers.return_path_domain and headers.from_domain:
            checks['return_path_match'] = (
                headers.return_path_domain.lower() == headers.from_domain.lower()
            )
        
        # Identify issues
        if not checks['spf_aligned']:
            checks['authentication_issues'].append('SPF failed or not configured')
        if not checks['dkim_aligned']:
            checks['authentication_issues'].append('DKIM failed or not configured')
        if not checks['dmarc_aligned']:
            checks['authentication_issues'].append('DMARC failed or not configured')
        if not checks['return_path_match']:
            checks['authentication_issues'].append('Return-Path does not match From domain')
        
        return checks
    
    def analyze(self, email_content: str, raw_headers: Optional[str] = None) -> Dict:
        """
        Analyze email for phishing indicators.
        
        Args:
            email_content: Email body content (can include HTML)
            raw_headers: Optional raw email headers
        
        Returns:
            Dict with risk score, indicators, and authentication results
        """
        # Parse headers
        if raw_headers:
            headers = self._extract_headers(raw_headers)
        else:
            # Try to extract from content
            headers = self._extract_headers(email_content)
        
        indicators = []
        
        # Authentication checks
        auth_checks = self._check_authentication_alignment(headers)
        
        # Check DNS records
        if headers.from_domain:
            dns_records = self._check_dns_records(headers.from_domain)
        else:
            dns_records = {}
        
        # Build authentication indicator
        auth_issues = auth_checks['authentication_issues']
        if auth_issues:
            indicators.extend(auth_issues)
        
        # Suspicious sender patterns
        for pattern in self.SUSPICIOUS_SENDER_PATTERNS:
            if re.match(pattern, headers.from_address, re.IGNORECASE):
                indicators.append(f"Suspicious sender pattern: {headers.from_address}")
                break
        
        # Urgency analysis
        urgency_score = self._calculate_urgency_score(email_content)
        if urgency_score > 0.01:  # More than 1% urgency keywords
            indicators.append(f"High urgency keyword density ({urgency_score:.2f}%)")
        
        # HTML/Text ratio
        html_ratio = self._calculate_html_text_ratio(email_content)
        if html_ratio > 0.3:
            indicators.append(f"High HTML-to-text ratio ({html_ratio:.2f}) - possible obfuscation")
        
        # Link analysis
        links = self._extract_links(email_content)
        suspicious_links = [l for l in links if l['mismatch']]
        if suspicious_links:
            indicators.append(f"Found {len(suspicious_links)} link(s) with visible URL mismatch")
        
        # Get Naive Bayes prediction if model is fitted
        if self.is_fitted:
            X = self._extract_features(email_content, headers)
            # Get probability of phishing (class 1)
            proba = self.model.predict_proba(X)[0]
            # Convert to risk score (0-100)
            base_score = int(proba[1] * 100) if len(proba) > 1 else 50
        else:
            # Heuristic fallback
            base_score = self._heuristic_score(
                auth_checks, urgency_score, html_ratio, len(suspicious_links)
            )
        
        # Authentication penalty
        auth_failures = sum([
            not auth_checks['spf_aligned'],
            not auth_checks['dkim_aligned'],
            not auth_checks['dmarc_aligned'],
            not auth_checks['return_path_match']
        ])
        base_score += auth_failures * 10
        
        # Clamp score
        risk_score = max(0, min(100, base_score))
        
        return {
            "score": risk_score,
            "confidence": round(0.75 + (abs(50 - risk_score) / 200), 2),
            "indicators": indicators,
            "sender_authenticity": "spoofed" if auth_failures >= 2 else "legitimate",
            "authentication": {
                "spf": headers.spf_result or "not_checked",
                "dkim": headers.dkim_result or "not_checked",
                "dmarc": headers.dmarc_result or "not_checked",
                "return_path_match": auth_checks['return_path_match']
            },
            "suspicious_elements": {
                "urgency_score": urgency_score,
                "html_ratio": html_ratio,
                "suspicious_links_count": len(suspicious_links),
                "suspicious_links": suspicious_links[:5]  # Limit details
            }
        }
    
    def _heuristic_score(
        self, auth_checks: Dict, urgency_score: float,
        html_ratio: float, suspicious_links: int
    ) -> int:
        """Calculate heuristic score when model not available."""
        score = 0
        
        # Authentication failures
        if not auth_checks['spf_aligned']:
            score += 15
        if not auth_checks['dkim_aligned']:
            score += 15
        if not auth_checks['dmarc_aligned']:
            score += 15
        if not auth_checks['return_path_match']:
            score += 20
        
        # High urgency
        if urgency_score > 0.02:
            score += 15
        
        # High HTML ratio (obfuscation)
        if html_ratio > 0.5:
            score += 10
        
        # Suspicious links
        score += suspicious_links * 15
        
        return min(100, score)
    
    def train(self, emails: List[str], labels: List[int]):
        """
        Train Naive Bayes classifier.
        
        Args:
            emails: List of email contents
            labels: List of labels (0 = benign, 1 = phishing)
        """
        print(f"Training Email Forensic Analyzer on {len(emails)} emails...")
        
        # Vectorize emails
        X = self.vectorizer.transform(emails)
        
        # Train model
        self.model.fit(X, labels)
        self.is_fitted = True
        
        # Save model
        self._save_model()
        
        print(f"Training complete. Model saved to {self.model_path}")
    
    def partial_train(self, emails: List[str], labels: List[int]):
        """
        Incremental training with partial_fit (memory efficient).
        
        Args:
            emails: Batch of email contents
            labels: Batch of labels
        """
        if not self.is_fitted:
            # First training
            self.train(emails, labels)
            return
        
        # Vectorize batch
        X_batch = self.vectorizer.transform(emails)
        
        # Partial fit
        self.model.partial_fit(X_batch, labels, classes=[0, 1])
        
        self._save_model()
    
    def _save_model(self):
        """Save model to disk."""
        import os
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        
        joblib.dump({
            'model': self.model,
            'vectorizer_features': settings.EMAIL_VECTORIZER_FEATURES
        }, self.model_path, compress=3)
