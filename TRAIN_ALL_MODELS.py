#!/usr/bin/env python3
"""
================================================================================
PhishPulse - Complete Model Training Script
================================================================================

This script trains all 3 AI models for PhishPulse:
- Model A: URL Lexical Analyzer (Isolation Forest)
- Model B: Email Forensic Analyzer (Naive Bayes)
- Model C: Visual Phishing Detector (ORB + pHash)

Requirements: pip install -r requirements.txt

Usage: python3 TRAIN_ALL_MODELS.py
================================================================================
"""

import os
import sys
import csv
import pickle
import gzip
import sqlite3
import numpy as np
from pathlib import Path

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Try to import optional dependencies
try:
    from sklearn.ensemble import IsolationForest
    from sklearn.feature_extraction.text import HashingVectorizer
    from sklearn.naive_bayes import MultinomialNB
    import cv2
    import imagehash
    from PIL import Image
    SKLEARN_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Missing dependency: {e}")
    print("Please install requirements: pip install -r requirements.txt")
    SKLEARN_AVAILABLE = False


# =============================================================================
# CONFIGURATION
# =============================================================================

DATA_DIR = "data"
MODELS_DIR = "models"

# Data paths
URL_DATA = f"{DATA_DIR}/urls/majestic_million.csv"
EMAIL_DATA = f"{DATA_DIR}/emails/enron_spam_data.csv"
BRAND_DIR = f"{DATA_DIR}/brand_logos"

# Model output paths
URL_MODEL = f"{MODELS_DIR}/url_isolation_forest.pkl.gz"
EMAIL_MODEL = f"{MODELS_DIR}/email_nb_model.pkl"
EMAIL_VECTORIZER = f"{MODELS_DIR}/email_vectorizer.pkl"
VISUAL_DB = f"{MODELS_DIR}/visual_hashes.db"

# Training parameters
URL_BATCH_SIZE = 5000
URL_N_ESTIMATORS = 100
URL_CONTAMINATION = 0.1
EMAIL_BATCH_SIZE = 500
EMAIL_MAX_FEATURES = 1024


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def ensure_dirs():
    """Create necessary directories."""
    os.makedirs(MODELS_DIR, exist_ok=True)
    print(f"✓ Ensured directories exist")


def print_header(text):
    """Print formatted header."""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")


def print_section(text):
    """Print section header."""
    print(f"\n{'─'*70}")
    print(f"  {text}")
    print(f"{'─'*70}\n")


# =============================================================================
# MODEL A: URL LEXICAL ANALYZER
# =============================================================================

class URLFeatureExtractor:
    """Extract features from URLs for Isolation Forest."""
    
    import re
    from urllib.parse import urlparse
    
    SUSPICIOUS_TLDS = {
        '.tk': 1, '.ml': 1, '.cf': 1, '.ga': 1, '.gq': 1,
        '.xyz': 0.8, '.top': 0.8, '.work': 0.6, '.date': 0.6,
        '.racing': 0.6, '.loan': 0.8, '.download': 0.6
    }
    
    @classmethod
    def extract(cls, url):
        """Extract numerical features from URL."""
        try:
            from urllib.parse import urlparse
            import re
            
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            path = parsed.path.lower()
            
            features = [
                # Length features
                len(url),
                len(domain),
                len(path),
                
                # Character counts
                url.count('.'),
                url.count('-'),
                url.count('_'),
                url.count('/'),
                url.count('?'),
                url.count('='),
                url.count('&'),
                
                # Security indicators
                1 if parsed.scheme == 'https' else 0,
                
                # Domain features
                len(domain.split('.')) if domain else 0,
                sum(c.isdigit() for c in domain),
                sum(c.isalpha() for c in domain),
                
                # Path features
                path.count('%'),  # URL encoding
                path.count('.') if path else 0,
                
                # Suspicious patterns
                1 if '@' in url else 0,
                1 if 'ip' in domain else 0,
                
                # Entropy approximation (character variety)
                len(set(url.lower())) / len(url) if url else 0,
                
                # TLD risk score
                cls.SUSPICIOUS_TLDS.get('.' + domain.split('.')[-1], 0) if domain else 0,
            ]
            
            return np.array(features, dtype=np.float32)
        except Exception:
            return np.zeros(21, dtype=np.float32)


def train_model_a():
    """Train URL Lexical Analyzer (Isolation Forest)."""
    print_section("MODEL A: URL Lexical Analyzer (Isolation Forest)")
    
    # Check if data exists
    if not os.path.exists(URL_DATA):
        print(f"❌ URL data not found: {URL_DATA}")
        print("   Please download Majestic Million first.")
        return False
    
    print(f"📁 Loading URLs from: {URL_DATA}")
    
    # Load URLs from CSV (Majestic Million format: GlobalRank,TldRank,Domain,...)
    urls = []
    try:
        with open(URL_DATA, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for i, row in enumerate(reader):
                if i >= 100000:  # Limit to 100k for faster training
                    break
                if len(row) >= 3:
                    domain = row[2].strip()
                    if domain:
                        urls.append(f"https://{domain}")
    except Exception as e:
        print(f"❌ Error loading URLs: {e}")
        return False
    
    print(f"✓ Loaded {len(urls):,} URLs")
    
    # Extract features
    print(f"🔧 Extracting features...")
    X = np.array([URLFeatureExtractor.extract(url) for url in urls])
    print(f"✓ Feature matrix shape: {X.shape}")
    
    # Train Isolation Forest
    print(f"🧠 Training Isolation Forest...")
    print(f"   Parameters: n_estimators={URL_N_ESTIMATORS}, contamination={URL_CONTAMINATION}")
    
    model = IsolationForest(
        n_estimators=URL_N_ESTIMATORS,
        contamination=URL_CONTAMINATION,
        max_samples='auto',
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X)
    
    # Save model
    print(f"💾 Saving model to: {URL_MODEL}")
    os.makedirs(os.path.dirname(URL_MODEL), exist_ok=True)
    with gzip.open(URL_MODEL, 'wb') as f:
        pickle.dump({
            'model': model,
            'feature_names': [
                'url_length', 'domain_length', 'path_length',
                'dot_count', 'dash_count', 'underscore_count',
                'slash_count', 'query_count', 'eq_count', 'amp_count',
                'is_https', 'domain_parts', 'domain_digits', 'domain_alpha',
                'url_encoding_count', 'path_dots', 'has_at', 'has_ip',
                'entropy', 'tld_risk'
            ]
        }, f)
    
    # Calculate statistics
    scores = model.decision_function(X)
    print(f"\n📊 Training Statistics:")
    print(f"   Mean outlier score: {scores.mean():.4f}")
    print(f"   Std deviation: {scores.std():.4f}")
    print(f"   Anomalies detected: {(scores < 0).sum():,} ({(scores < 0).mean()*100:.1f}%)")
    
    print(f"\n✅ Model A training complete!")
    return True


# =============================================================================
# MODEL B: EMAIL FORENSIC ANALYZER
# =============================================================================

def train_model_b():
    """Train Email Forensic Analyzer (Naive Bayes)."""
    print_section("MODEL B: Email Forensic Analyzer (Naive Bayes)")
    
    # Check if data exists
    if not os.path.exists(EMAIL_DATA):
        print(f"❌ Email data not found: {EMAIL_DATA}")
        return False
    
    print(f"📁 Loading emails from: {EMAIL_DATA}")
    
    # Load emails from Enron-Spam CSV
    emails = []
    labels = []
    
    try:
        with open(EMAIL_DATA, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f)
            for row in reader:
                subject = row.get('Subject', '')
                message = row.get('Message', '')
                label = row.get('Spam/Ham', '').lower().strip()
                
                # Combine subject and message
                text = f"Subject: {subject}\n\n{message}"
                
                if text.strip() and label in ['ham', 'spam']:
                    emails.append(text)
                    labels.append(0 if label == 'ham' else 1)
        
        if len(emails) == 0:
            raise ValueError("No valid emails found")
            
    except Exception as e:
        print(f"❌ Error loading emails: {e}")
        return False
    
    print(f"✓ Loaded {len(emails):,} emails")
    print(f"   Ham (benign): {labels.count(0):,}")
    print(f"   Spam (phishing): {labels.count(1):,}")
    
    # Create vectorizer
    print(f"🔧 Creating vectorizer (max_features={EMAIL_MAX_FEATURES})...")
    vectorizer = HashingVectorizer(
        n_features=EMAIL_MAX_FEATURES,
        alternate_sign=False,
        ngram_range=(1, 2)
    )
    
    # Train Naive Bayes with partial_fit for memory efficiency
    print(f"🧠 Training Multinomial Naive Bayes...")
    model = MultinomialNB()
    
    # Process in batches
    n_batches = (len(emails) + EMAIL_BATCH_SIZE - 1) // EMAIL_BATCH_SIZE
    
    for i in range(0, len(emails), EMAIL_BATCH_SIZE):
        batch_emails = emails[i:i+EMAIL_BATCH_SIZE]
        batch_labels = labels[i:i+EMAIL_BATCH_SIZE]
        
        X_batch = vectorizer.transform(batch_emails)
        
        if i == 0:
            model.partial_fit(X_batch, batch_labels, classes=[0, 1])
        else:
            model.partial_fit(X_batch, batch_labels)
        
        batch_num = i // EMAIL_BATCH_SIZE + 1
        if batch_num % 5 == 0 or batch_num == n_batches:
            print(f"   Batch {batch_num}/{n_batches} complete")
    
    # Save model and vectorizer
    print(f"💾 Saving model to: {EMAIL_MODEL}")
    os.makedirs(os.path.dirname(EMAIL_MODEL), exist_ok=True)
    
    with open(EMAIL_MODEL, 'wb') as f:
        pickle.dump(model, f)
    
    with open(EMAIL_VECTORIZER, 'wb') as f:
        pickle.dump(vectorizer, f)
    
    # Calculate accuracy on training data
    X_all = vectorizer.transform(emails)
    predictions = model.predict(X_all)
    accuracy = (predictions == np.array(labels)).mean()
    
    print(f"\n📊 Training Statistics:")
    print(f"   Training accuracy: {accuracy*100:.1f}%")
    print(f"   Ham classified as ham: {((predictions == 0) & (np.array(labels) == 0)).sum():,}")
    print(f"   Spam classified as spam: {((predictions == 1) & (np.array(labels) == 1)).sum():,}")
    
    print(f"\n✅ Model B training complete!")
    return True


# =============================================================================
# MODEL C: VISUAL PHISHING DETECTOR
# =============================================================================

def train_model_c():
    """Train Visual Phishing Detector (pHash database)."""
    print_section("MODEL C: Visual Phishing Detector (Perceptual Hashing)")
    
    # Check if brand logos exist
    if not os.path.exists(BRAND_DIR):
        print(f"❌ Brand logos not found: {BRAND_DIR}")
        return False
    
    brand_dirs = [d for d in os.listdir(BRAND_DIR) 
                  if os.path.isdir(os.path.join(BRAND_DIR, d))]
    
    if not brand_dirs:
        print(f"❌ No brand directories found in: {BRAND_DIR}")
        return False
    
    print(f"📁 Found {len(brand_dirs)} brand directories")
    
    # Create SQLite database for hashes
    print(f"🔧 Creating hash database: {VISUAL_DB}")
    os.makedirs(os.path.dirname(VISUAL_DB), exist_ok=True)
    
    conn = sqlite3.connect(VISUAL_DB)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS brand_hashes (
            id INTEGER PRIMARY KEY,
            brand TEXT NOT NULL,
            hash TEXT NOT NULL,
            algorithm TEXT DEFAULT 'phash'
        )
    ''')
    
    cursor.execute('DELETE FROM brand_hashes')
    
    # Process each brand
    total_hashes = 0
    
    for brand in sorted(brand_dirs):
        brand_path = os.path.join(BRAND_DIR, brand)
        image_files = [f for f in os.listdir(brand_path) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg', '.ico', '.gif'))]
        
        if not image_files:
            continue
            
        print(f"   Processing {brand}: {len(image_files)} images")
        
        for img_file in image_files:
            img_path = os.path.join(brand_path, img_file)
            
            try:
                # Load and convert image
                img = Image.open(img_path)
                
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Compute pHash
                hash_val = str(imagehash.phash(img))
                
                # Save to database
                cursor.execute(
                    'INSERT INTO brand_hashes (brand, hash, algorithm) VALUES (?, ?, ?)',
                    (brand.lower(), hash_val, 'phash')
                )
                total_hashes += 1
                
            except Exception as e:
                print(f"      ⚠️  Error processing {img_file}: {e}")
    
    conn.commit()
    conn.close()
    
    print(f"\n📊 Database Statistics:")
    print(f"   Total brands: {len(brand_dirs)}")
    print(f"   Total hashes: {total_hashes:,}")
    print(f"   Average hashes per brand: {total_hashes // len(brand_dirs)}")
    
    print(f"\n✅ Model C training complete!")
    return True


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main():
    """Main training function."""
    print_header("PhishPulse - Complete Model Training")
    
    # Check dependencies
    if not SKLEARN_AVAILABLE:
        print("❌ Required dependencies not available!")
        print("\nPlease install requirements:")
        print("   pip install -r requirements.txt")
        return 1
    
    # Ensure directories
    ensure_dirs()
    
    # Track results
    results = {
        'Model A (URL)': False,
        'Model B (Email)': False,
        'Model C (Visual)': False
    }
    
    # Train Model A
    try:
        results['Model A (URL)'] = train_model_a()
    except Exception as e:
        print(f"\n❌ Model A training failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Train Model B
    try:
        results['Model B (Email)'] = train_model_b()
    except Exception as e:
        print(f"\n❌ Model B training failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Train Model C
    try:
        results['Model C (Visual)'] = train_model_c()
    except Exception as e:
        print(f"\n❌ Model C training failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Final summary
    print_header("Training Summary")
    
    for model, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"   {model}: {status}")
    
    all_success = all(results.values())
    
    if all_success:
        print("\n🎉 All models trained successfully!")
        print("\nYou can now start the backend:")
        print("   uvicorn backend.app.main:app --reload")
    else:
        print("\n⚠️  Some models failed to train.")
        print("   Check the errors above and try again.")
    
    print("\n" + "="*70)
    
    return 0 if all_success else 1


if __name__ == "__main__":
    sys.exit(main())
