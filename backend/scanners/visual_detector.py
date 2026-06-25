"""Model C: Visual Phishing Detector - ORB + Perceptual Hashing (pHash)"""

import io
import cv2
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import imagehash
from PIL import Image
import sqlite3
import joblib
import json
import os
import uuid


@dataclass
class VisualMatch:
    brand_name: str
    confidence: float
    match_type: str
    hamming_distance: Optional[int] = None
    orb_matches: Optional[int] = None


class VisualPhishingDetector:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or "models/visual_hashes.db"
        self.orb = cv2.ORB_create(nfeatures=500)
        self.phash_threshold = 10
        self.brand_hashes: Dict[str, List[str]] = {}
        self.brand_orb_features: Dict[str, List] = {}
        self._load_brand_database()

    def _load_brand_database(self):
        """Load brand hashes from SQLite database."""
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS visual_hashes (
                    id TEXT PRIMARY KEY,
                    brand_name TEXT NOT NULL,
                    phash TEXT NOT NULL,
                    orb_descriptors BLOB,
                    orb_shape TEXT,
                    image_path TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            
            cursor.execute("SELECT brand_name, phash FROM visual_hashes")
            for row in cursor.fetchall():
                brand, phash = row[0], row[1]
                if brand not in self.brand_hashes:
                    self.brand_hashes[brand] = []
                self.brand_hashes[brand].append(phash)
            
            cursor.execute("SELECT brand_name, orb_descriptors, orb_shape FROM visual_hashes WHERE orb_descriptors IS NOT NULL")
            for row in cursor.fetchall():
                brand, desc_blob, shape_str = row
                if desc_blob and shape_str:
                    try:
                        shape = tuple(json.loads(shape_str))
                        descriptors = np.frombuffer(desc_blob, dtype=np.uint8).reshape(shape)
                        if brand not in self.brand_orb_features:
                            self.brand_orb_features[brand] = []
                        self.brand_orb_features[brand].append(descriptors)
                    except Exception:
                        continue
            
            conn.close()
            total = sum(len(v) for v in self.brand_hashes.values())
            print(f"Loaded {total} brand hashes")
            
        except Exception as e:
            print(f"Warning: Could not load brand database: {e}")
            self._init_default_brands()

    def _init_default_brands(self):
        self.brand_hashes = {
            "paypal": [], "microsoft": [], "google": [], "apple": [],
            "amazon": [], "facebook": [], "netflix": [], "linkedin": [],
            "dropbox": [], "adobe": []
        }

    def _compute_phash(self, image: np.ndarray) -> imagehash.ImageHash:
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil = Image.fromarray(rgb)
        return imagehash.phash(pil)

    def _compute_orb_features(self, image: np.ndarray) -> Tuple[List, np.ndarray]:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return self.orb.detectAndCompute(gray, None)

    def _hamming_distance(self, h1: imagehash.ImageHash, h2: imagehash.ImageHash) -> int:
        return h1 - h2

    def _match_orb_features(self, desc1: np.ndarray, desc2: np.ndarray) -> int:
        if desc1 is None or desc2 is None:
            return 0
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        try:
            matches = bf.match(desc1, desc2)
            matches = sorted(matches, key=lambda x: x.distance)
            return sum(1 for m in matches if m.distance < 50)
        except Exception:
            return 0

    def analyze_image(self, image: np.ndarray) -> Dict:
        indicators = []
        matches = []
        
        img_phash = self._compute_phash(image)
        img_keypoints, img_descriptors = self._compute_orb_features(image)
        
        for brand, hashes in self.brand_hashes.items():
            min_hamming = float('inf')
            for brand_hash_hex in hashes:
                try:
                    brand_hash = imagehash.hex_to_hash(brand_hash_hex)
                    distance = self._hamming_distance(img_phash, brand_hash)
                    min_hamming = min(min_hamming, distance)
                except Exception:
                    continue
            
            if min_hamming <= self.phash_threshold:
                confidence = 1.0 - (min_hamming / 64.0)
                matches.append(VisualMatch(brand_name=brand, confidence=confidence, match_type="phash", hamming_distance=min_hamming))
        
        for brand, descriptors_list in self.brand_orb_features.items():
            if img_descriptors is None:
                continue
            max_matches = 0
            for brand_desc in descriptors_list:
                if brand_desc is None:
                    continue
                match_count = self._match_orb_features(img_descriptors, brand_desc)
                max_matches = max(max_matches, match_count)
            
            if max_matches > 20:
                orb_confidence = min(1.0, max_matches / 100.0)
                existing = next((m for m in matches if m.brand_name == brand), None)
                if existing:
                    existing.confidence = max(existing.confidence, orb_confidence)
                    existing.match_type = "combined"
                    existing.orb_matches = max_matches
                else:
                    matches.append(VisualMatch(brand_name=brand, confidence=orb_confidence, match_type="orb", orb_matches=max_matches))
        
        risk_score, impersonated_brand = self._calculate_risk_from_matches(matches)
        
        return {
            "score": risk_score,
            "confidence": round(0.6 + (risk_score / 250), 2),
            "indicators": indicators,
            "impersonated_brand": impersonated_brand,
            "visual_matches": [{"brand": m.brand_name, "confidence": round(m.confidence, 4), "match_type": m.match_type} for m in matches[:5]],
            "form_fields_detected": 0,
            "ssl_badge_info": {"lock_detected": False, "confidence": 0},
            "phash": str(img_phash)
        }

    def _calculate_risk_from_matches(self, matches: List[VisualMatch]) -> Tuple[int, str]:
        if not matches:
            return 0, None
        best = max(matches, key=lambda m: m.confidence)
        if best.confidence > 0.85:
            return 90, best.brand_name
        elif best.confidence > 0.70:
            return 70, best.brand_name
        elif best.confidence > 0.50:
            return 50, best.brand_name
        else:
            return 30, best.brand_name

    def analyze_bytes(self, image_bytes: bytes) -> Dict:
        try:
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if image is None:
                raise ValueError("Could not decode image")
            return self.analyze_image(image)
        except Exception as e:
            return {"score": 0, "error": str(e), "indicators": [], "impersonated_brand": None}

    def analyze_file(self, image_path: str) -> Dict:
        image = cv2.imread(image_path)
        if image is None:
            return {"score": 0, "error": "Could not load image", "indicators": [], "impersonated_brand": None}
        return self.analyze_image(image)
