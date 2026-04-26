"""
Model C: Visual Phishing Detector
Unsupervised computer vision using ORB + Perceptual Hashing (pHash).

Purpose: Visual brand impersonation detection without labeled phishing imagery.
"""

import io
import cv2
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import imagehash
from PIL import Image
import sqlite3
import joblib

from backend.app.config import settings


@dataclass
class VisualMatch:
    """Visual match result."""
    brand_name: str
    confidence: float
    match_type: str  # 'phash', 'orb', 'combined'
    hamming_distance: Optional[int] = None
    orb_matches: Optional[int] = None


class VisualPhishingDetector:
    """
    Visual Phishing Detector using ORB and perceptual hashing.
    
    Features:
    - ORB feature extraction and matching
    - 64-bit perceptual hashing (pHash)
    - Form field detection
    - SSL badge spoofing detection
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """Initialize visual detector with hash database."""
        self.db_path = db_path or settings.VISUAL_HASHES_DB
        self.orb = cv2.ORB_create(nfeatures=settings.VISUAL_ORB_FEATURES)
        self.phash_threshold = settings.VISUAL_PHASH_THRESHOLD
        
        # Brand logo database (instance-specific cache)
        self.brand_hashes: Dict[str, List[str]] = {}  # brand_name -> list of phash hex strings
        self.brand_orb_features: Dict[str, List] = {}  # brand_name -> list of ORB descriptors
        
        # Load brand hashes
        self._load_brand_database()
    
    def _load_brand_database(self):
        """Load brand hashes from SQLite database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT brand_name, phash FROM visual_hashes")
            rows = cursor.fetchall()
            
            for brand, phash_hex in rows:
                if brand not in self.brand_hashes:
                    self.brand_hashes[brand] = []
                self.brand_hashes[brand].append(phash_hex)
            
            conn.close()
            print(f"Loaded {len(rows)} brand hashes from database")
        except Exception as e:
            print(f"Warning: Could not load brand database: {e}")
            # Initialize with default brands
            self._init_default_brands()
    
    def _init_default_brands(self):
        """Initialize with minimal default brand set."""
        # These would normally be loaded from the database
        # Placeholder for when DB is empty
        self.brand_hashes = {
            "paypal": [],
            "microsoft": [],
            "google": [],
            "apple": [],
            "amazon": [],
            "facebook": [],
            "netflix": [],
            "linkedin": [],
            "dropbox": [],
            "adobe": []
        }
    
    def _compute_phash(self, image: np.ndarray) -> imagehash.ImageHash:
        """Compute perceptual hash of image."""
        # Convert OpenCV BGR to PIL RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_image)
        return imagehash.phash(pil_image)
    
    def _compute_orb_features(self, image: np.ndarray) -> Tuple[List, np.ndarray]:
        """Compute ORB keypoints and descriptors."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        keypoints, descriptors = self.orb.detectAndCompute(gray, None)
        return keypoints, descriptors
    
    def _hamming_distance(self, hash1: imagehash.ImageHash, hash2: imagehash.ImageHash) -> int:
        """Calculate Hamming distance between two hashes."""
        return hash1 - hash2
    
    def _match_orb_features(
        self, desc1: np.ndarray, desc2: np.ndarray
    ) -> int:
        """Match ORB features using Brute-Force Hamming distance."""
        if desc1 is None or desc2 is None:
            return 0
        
        # BFMatcher with Hamming distance (ORB uses binary descriptors)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        
        try:
            matches = bf.match(desc1, desc2)
            # Sort by distance
            matches = sorted(matches, key=lambda x: x.distance)
            # Count good matches (distance < threshold)
            good_matches = sum(1 for m in matches if m.distance < 50)
            return good_matches
        except Exception:
            return 0
    
    def _detect_form_fields(self, image: np.ndarray) -> List[Dict]:
        """Detect potential credential input fields."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Use edge detection to find rectangular regions
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        form_fields = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            
            # Filter for input-field-like rectangles
            aspect_ratio = float(w) / h if h > 0 else 0
            if 2 < aspect_ratio < 10 and 20 < h < 60 and w > 100:
                form_fields.append({
                    "x": x,
                    "y": y,
                    "width": w,
                    "height": h,
                    "aspect_ratio": aspect_ratio
                })
        
        return form_fields
    
    def _detect_ssl_badge(self, image: np.ndarray) -> Dict:
        """Detect potential SSL badge spoofing."""
        # Look for lock icons, security badges
        # This is a simplified version - production would use template matching
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Template matching for lock icon patterns
        # Load templates (would be loaded from files in production)
        lock_detected = False
        confidence = 0.0
        
        # Simple heuristic: look for small square regions that might be icons
        # In production, this would use actual lock icon templates
        height, width = gray.shape
        roi = gray[int(height*0.8):, :]  # Bottom area where lock usually appears
        
        # Check for high-contrast small regions (potential icons)
        edges = cv2.Canny(roi, 100, 200)
        icon_score = np.sum(edges > 0) / edges.size
        
        if icon_score > 0.01:  # Some edge density
            lock_detected = True
            confidence = min(1.0, icon_score * 10)
        
        return {
            "lock_detected": lock_detected,
            "confidence": confidence,
            "is_spoofed": False  # Would need more analysis
        }
    
    def _calculate_risk_from_matches(self, matches: List[VisualMatch]) -> Tuple[int, str]:
        """Calculate risk score from visual matches."""
        if not matches:
            return 0, None
        
        # Get best match
        best = max(matches, key=lambda m: m.confidence)
        
        # Confidence threshold for brand impersonation
        if best.confidence > 0.85:
            return 90, best.brand_name
        elif best.confidence > 0.70:
            return 70, best.brand_name
        elif best.confidence > 0.50:
            return 50, best.brand_name
        else:
            return 30, best.brand_name
    
    def analyze_image(self, image: np.ndarray) -> Dict:
        """
        Analyze image for visual phishing indicators.
        
        Args:
            image: OpenCV BGR image (numpy array)
        
        Returns:
            Dict with risk score and match details
        """
        indicators = []
        matches = []
        
        # Compute pHash
        img_phash = self._compute_phash(image)
        
        # Compute ORB features
        img_keypoints, img_descriptors = self._compute_orb_features(image)
        
        # Compare against brand database
        for brand, hashes in self.brand_hashes.items():
            # pHash comparison
            min_hamming = float('inf')
            for brand_hash_hex in hashes:
                try:
                    brand_hash = imagehash.hex_to_hash(brand_hash_hex)
                    distance = self._hamming_distance(img_phash, brand_hash)
                    min_hamming = min(min_hamming, distance)
                except Exception:
                    continue
            
            # Convert Hamming distance to confidence (lower = better match)
            if min_hamming <= self.phash_threshold:
                phash_confidence = 1.0 - (min_hamming / 64.0)
                matches.append(VisualMatch(
                    brand_name=brand,
                    confidence=phash_confidence,
                    match_type="phash",
                    hamming_distance=min_hamming
                ))
        
        # ORB matching (if we have brand ORB features)
        for brand, descriptors_list in self.brand_orb_features.items():
            if img_descriptors is None:
                continue
            
            max_matches = 0
            for brand_desc in descriptors_list:
                if brand_desc is None:
                    continue
                match_count = self._match_orb_features(img_descriptors, brand_desc)
                max_matches = max(max_matches, match_count)
            
            # Convert match count to confidence
            if max_matches > 20:  # Threshold for significant matches
                orb_confidence = min(1.0, max_matches / 100.0)
                
                # Check if brand already has pHash match
                existing = next((m for m in matches if m.brand_name == brand), None)
                if existing:
                    # Combine scores
                    existing.confidence = max(existing.confidence, orb_confidence)
                    existing.match_type = "combined"
                    existing.orb_matches = max_matches
                else:
                    matches.append(VisualMatch(
                        brand_name=brand,
                        confidence=orb_confidence,
                        match_type="orb",
                        orb_matches=max_matches
                    ))
        
        # Detect form fields
        form_fields = self._detect_form_fields(image)
        if form_fields:
            indicators.append(f"Detected {len(form_fields)} potential form field(s)")
        
        # Detect SSL badge
        ssl_info = self._detect_ssl_badge(image)
        if ssl_info['lock_detected']:
            indicators.append("SSL lock icon detected (verify authenticity)")
        
        # Calculate risk score
        risk_score, impersonated_brand = self._calculate_risk_from_matches(matches)
        
        # Add form field risk
        if form_fields and risk_score > 50:
            indicators.append("Form fields detected on suspicious domain")
            risk_score = min(100, risk_score + 10)
        
        # Format matches for output
        match_dicts = [
            {
                "brand": m.brand_name,
                "confidence": round(m.confidence, 4),
                "match_type": m.match_type,
                "hamming_distance": m.hamming_distance,
                "orb_matches": m.orb_matches
            }
            for m in matches
        ]
        
        return {
            "score": risk_score,
            "confidence": round(0.6 + (risk_score / 250), 2),  # Base + scaled
            "indicators": indicators,
            "impersonated_brand": impersonated_brand,
            "visual_matches": match_dicts[:5],  # Top 5 matches
            "form_fields_detected": len(form_fields),
            "ssl_badge_info": ssl_info,
            "phash": str(img_phash)
        }
    
    def analyze_file(self, image_path: str) -> Dict:
        """Analyze image file."""
        image = cv2.imread(image_path)
        if image is None:
            return {
                "score": 0,
                "error": "Could not load image",
                "indicators": [],
                "impersonated_brand": None
            }
        return self.analyze_image(image)
    
    def analyze_bytes(self, image_bytes: bytes) -> Dict:
        """Analyze image from bytes."""
        try:
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if image is None:
                raise ValueError("Could not decode image")
            return self.analyze_image(image)
        except Exception as e:
            return {
                "score": 0,
                "error": str(e),
                "indicators": [],
                "impersonated_brand": None
            }
    
    def add_brand_logo(self, brand_name: str, image_path: str):
        """Add a brand logo to the database."""
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        # Compute pHash
        phash = self._compute_phash(image)
        phash_hex = str(phash)
        
        # Compute ORB features
        _, descriptors = self._compute_orb_features(image)
        
        # Save to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS visual_hashes (
                id TEXT PRIMARY KEY,
                brand_name TEXT NOT NULL,
                phash TEXT NOT NULL,
                image_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        import uuid
        cursor.execute('''
            INSERT INTO visual_hashes (id, brand_name, phash, image_path)
            VALUES (?, ?, ?, ?)
        ''', (str(uuid.uuid4()), brand_name, phash_hex, image_path))
        
        conn.commit()
        conn.close()
        
        # Update in-memory cache
        if brand_name not in self.brand_hashes:
            self.brand_hashes[brand_name] = []
        self.brand_hashes[brand_name].append(phash_hex)
        
        if brand_name not in self.brand_orb_features:
            self.brand_orb_features[brand_name] = []
        self.brand_orb_features[brand_name].append(descriptors)
    
    def train(self, brand_logo_dir: str):
        """
        Train visual detector by building brand hash database.
        
        Args:
            brand_logo_dir: Directory containing brand logo subdirectories
        """
        import os
        
        print(f"Training Visual Phishing Detector from {brand_logo_dir}...")
        
        # Clear existing database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM visual_hashes')
        conn.commit()
        conn.close()
        
        self.brand_hashes = {}
        self.brand_orb_features = {}
        
        # Process each brand directory
        for brand_name in os.listdir(brand_logo_dir):
            brand_path = os.path.join(brand_logo_dir, brand_name)
            if not os.path.isdir(brand_path):
                continue
            
            print(f"Processing brand: {brand_name}")
            
            for filename in os.listdir(brand_path):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                    image_path = os.path.join(brand_path, filename)
                    try:
                        self.add_brand_logo(brand_name, image_path)
                    except Exception as e:
                        print(f"  Error processing {filename}: {e}")
        
        print(f"Training complete. Added {sum(len(v) for v in self.brand_hashes.values())} brand hashes.")
