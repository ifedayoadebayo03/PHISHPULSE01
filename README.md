# PhishPulse v2.0

**Real-Time Multi-Modal Phishing Detection Engine**

*Hybrid Unsupervised Anomaly Detection + Supervised Forensic Analysis*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.103+-00a393.svg)](https://fastapi.tiangolo.com/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-f7931e.svg)](https://scikit-learn.org/)

> **PhantomSecDy Research Initiative | Detect the Undetectable**

---

## Executive Summary

PhishPulse is a production-grade, four-model ensemble cybersecurity framework engineered for real-time detection of phishing attacks across URL, email, and visual attack vectors. Architected specifically for resource-constrained environments (**7.4GB RAM, CPU-only inference**), it employs unsupervised anomaly detection (Isolation Forests, perceptual hashing) for zero-day threat discovery while leveraging supervised forensic analysis (Naive Bayes, heuristic engines) for known attack pattern recognition.

### Key Innovation

Unlike signature-based solutions or simple API wrappers, PhishPulse utilizes hybrid AI architecture—training Isolation Forests exclusively on benign data to detect novel structural anomalies, while employing ORB computer vision and TF-IDF classification for specific attack vectors. This achieves **80-89% accuracy** with millisecond-level inference latency.

### Academic Context

**CSC 405 - Artificial Intelligence in Cybersecurity**

This implementation demonstrates:
- Unsupervised zero-day detection
- Resource-constrained ML optimization  
- Multi-modal risk fusion with isotonic regression calibration

---

## Architecture Overview

```
Input: URL/Email/Screenshot
         ↓
      Router
         ↓
   ┌─────┴─────┬─────────────┬────────────────┐
   ↓           ↓             ↓                ↓
Model A     Model B      Model C          Model D
URL         Email        Visual           Risk
Analyzer    Forensics    Detector         Fusion
   │           │             │                │
   │           │             │                │
   ↓           ↓             ↓                ↓
Isolation   Naive Bayes   ORB/pHash      Weighted
Forest      + Headers     Perceptual     Ensemble
+ Regex                   Hashing        + Isotonic
                                            Regression
   └─────────┬─────────────┴────────────────┘
             ↓
      Risk Score 0-100
             ↓
    ┌────────┴────────┐
    ↓                 ↓
Classification    PDF Forensic
(Clean/           Report
Suspicious/
Malicious/
Critical)
```

---

## The Four AI Models

### Model A: URL Lexical Analyzer (Unsupervised)

**Algorithm:** Isolation Forest + Regex Heuristics  
**Type:** Unsupervised Anomaly Detection  
**Purpose:** Zero-day phishing detection via structural anomaly identification without pre-labeled malicious datasets

**Technical Implementation:**

| Feature | Description |
|---------|-------------|
| Shannon Entropy | Calculates character-level randomness for DGA detection |
| Levenshtein Distance | Dynamic programming string similarity to Alexa Top 1,000 (typosquatting) |
| Suspicious TLD | Weighted risk matrix (.tk +15, .ml +15, .xyz +10) |
| Subdomain Depth | Excessive nesting detection |

**Training Data:** 100k benign URLs from CommonCrawl WET files

**Output:** `url_risk_score` (0-100), `brand_impersonated`, `structural_anomalies`

### Model B: Email Forensic Analyzer (Supervised)

**Algorithm:** TF-IDF + Multinomial Naive Bayes + Header Heuristics  
**Type:** Supervised Classification  
**Purpose:** Authentication protocol validation and semantic content analysis

**Technical Implementation:**

| Feature | Description |
|---------|-------------|
| SPF/DKIM/DMARC | DNS validation with alignment checking |
| Return-Path Analysis | Header mismatch detection (spoofing indicator) |
| TF-IDF Vectorization | HashingVectorizer(n_features=1024) for memory efficiency |
| Urgency Keywords | "immediate action", "verify now", "account suspended" detection |

**Training Data:** Enron Dataset (500k benign) + PhishingCorpus (5k malicious)

### Model C: Visual Phishing Detector (Unsupervised)

**Algorithm:** ORB (Oriented FAST and Rotated BRIEF) + Perceptual Hashing (pHash)  
**Type:** Unsupervised Computer Vision  
**Purpose:** Visual brand impersonation detection without labeled phishing imagery

**Technical Implementation:**

| Feature | Description |
|---------|-------------|
| ORB Features | CPU-optimized keypoint detection (100x faster than SIFT) |
| Perceptual Hashing | 64-bit pHash with Hamming distance comparison |
| Form Detection | CV template matching for credential fields |
| SSL Badge Spoofing | Template matching for fraudulent "secure" icons |

**Training Data:** No malicious images required—unsupervised matching against legitimate brand database

### Model D: Risk Fusion Engine (Ensemble)

**Algorithm:** Weighted Voting + Isotonic Regression  
**Type:** Meta-Classifier Ensemble  
**Purpose:** Multi-modal signal aggregation with calibrated confidence intervals

**Weight Distribution:**
- URL Analysis: 30%
- Email Forensics: 35%
- Visual Detection: 35%

**Thresholds:**
- 0-30: Clean (Green)
- 31-60: Suspicious (Amber)
- 61-85: Malicious (Red)
- 86-100: Critical (Crimson)

---

## Project Structure

```
phishpulse/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI application entry
│   │   ├── config.py               # Settings, model paths, thresholds
│   │   └── dependencies.py         # DB session, auth middleware
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── scan.py         # POST /scan (orchestrates all 4 models)
│   │       │   ├── report.py       # PDF generation endpoints
│   │       │   └── health.py       # System status, model versions
│   │       └── api.py              # Router aggregation
│   ├── core/
│   │   ├── security.py             # CORS, rate limiting
│   │   └── logging.py              # Structured JSON logging
│   ├── scanners/                   # The 4 Model Implementations
│   │   ├── url_lexical.py          # Model A: Isolation Forest
│   │   ├── email_forensics.py      # Model B: Naive Bayes + headers
│   │   ├── visual_detector.py      # Model C: ORB + pHash (OpenCV)
│   │   └── risk_fusion.py          # Model D: Weighted ensemble
│   ├── services/
│   │   ├── pdf_generator.py        # ReportLab forensic reports (6-page)
│   │   ├── screenshot_service.py   # Playwright capture service
│   │   └── whois_lookup.py         # Domain intelligence
│   ├── database/
│   │   ├── models.py               # SQLAlchemy schemas (Scan, Report)
│   │   ├── crud.py                 # DB operations
│   │   └── session.py              # SQLite WAL mode configuration
│   └── training/                   # Retraining & Validation
│       ├── train_url_analyzer.py   # Unsupervised Isolation Forest
│       ├── train_email_model.py    # Supervised NB with partial_fit
│       ├── train_visual.py         # Brand hash generation
│       └── validate_models.py      # Time-based split validation
├── extension/                      # Cross-Browser Extension
│   ├── manifest.json               # Manifest V3 (Chrome/Firefox/Edge)
│   ├── background.js               # Service worker
│   ├── content.js                  # Gmail/Outlook DOM extractors
│   ├── popup.html                  # Risk gauge UI
│   ├── popup.js                    # Extension logic
│   ├── styles.css                  # PhantomSecDy styling
│   └── lib/
│       └── browser-polyfill.js     # webextension-polyfill
├── frontend/                       # React Admin Dashboard
│   └── src/
│       ├── components/
│       │   ├── RiskGauge.jsx       # D3.js radial gauge
│       │   └── ScanHistory.jsx     # Paginated scan timeline
│       ├── pages/
│       │   ├── Dashboard.jsx       # Real-time stats
│       │   ├── Reports.jsx         # PDF download manager
│       │   └── Settings.jsx        # Threshold configuration
│       └── services/
│           └── api.js              # Axios client
├── data/                           # Training datasets (gitignored)
├── models/                         # Trained binaries (gitignored)
├── reports/                        # Generated PDF forensics
├── requirements.txt                # Python dependencies
└── README.md                       # This documentation
```

---

## Installation

### Prerequisites

```bash
python3 --version  # >= 3.9 required
free -h            # >= 4GB available RAM recommended
df -h              # >= 5GB disk space
```

### Setup

```bash
# Clone repository
git clone https://github.com/phantomsecdy/phishpulse.git
cd phishpulse

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies (no cache for disk space optimization)
pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Initialize SQLite database
python3 -c "from backend.database.models import create_tables; create_tables()"

# Verify installation
python3 -c "import backend.scanners.url_lexical; print('✓ Models loadable')"
```

---

## Usage

### 1. Training the Models

#### Model A (URL Analyzer) - Unsupervised:

```bash
python3 backend/training/train_url_analyzer.py \
    --benign-data data/commoncrawl_top100k.csv \
    --contamination 0.1 \
    --output models/url_isolation_forest.pkl.gz
```

#### Model B (Email Analyzer) - Supervised:

```bash
python3 backend/training/train_email_model.py \
    --benign data/enron_emails.csv \
    --phishing data/phishing_emails.csv \
    --batch-size 500
```

#### Model C (Visual Detector) - Unsupervised:

```bash
# First, set up brand logos
python3 backend/training/train_visual.py --download-samples

# Add brand logos to data/brand_logos/{brand_name}/
# Then train
python3 backend/training/train_visual.py \
    --brand-dir data/brand_logos/ \
    --output models/visual_hashes.db
```

### 2. Starting the Backend

```bash
# Production mode (single worker due to RAM constraints)
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --workers 1

# Development mode with auto-reload
uvicorn backend.app.main:app --reload --port 8000
```

### 3. Browser Extension Setup

1. Navigate to `chrome://extensions/` (Chrome) or `about:debugging` (Firefox)
2. Enable "Developer Mode" → "Load Unpacked"
3. Select `phishpulse/extension/` directory
4. Configure API endpoint in popup settings: `http://localhost:8000`
5. Navigate to Gmail/Outlook—extension auto-injects risk indicators

### 4. React Dashboard

```bash
cd frontend/
npm install
npm start  # Runs on http://localhost:3000
```

---

## API Endpoints

### Unified Scan Endpoint

```http
POST /api/v1/scan
Content-Type: application/json

{
  "type": "url",
  "target": "http://paypa1-security-update.com/login",
  "options": {
    "screenshot": true,
    "generate_report": true
  }
}
```

**Response:**

```json
{
  "scan_id": "uuid-v4",
  "timestamp": "2024-01-06T14:30:00Z",
  "final_score": 87,
  "classification": "Critical",
  "confidence_interval": [0.82, 0.91],
  "model_breakdown": {
    "url_analyzer": {"score": 85, "weight": 0.30},
    "email_forensics": {"score": 0, "weight": 0.35},
    "visual_detector": {"score": 90, "weight": 0.35}
  },
  "indicators": [
    "High Levenshtein distance from paypal.com (distance: 2)",
    "Domain registered 2 days ago",
    "Visual match: PayPal logo detected with 94% confidence"
  ],
  "mitigation_steps": [
    "Block domain at firewall immediately",
    "Reset credentials if submitted",
    "Submit to PhishTank API"
  ],
  "report_url": "/api/v1/reports/download/scan_id.pdf"
}
```

### Health Check

```http
GET /api/v1/health/
```

### Model Information

```http
GET /api/v1/health/model-info
```

---

## Performance Benchmarks

| Model | Algorithm | Accuracy | Precision | Recall | Inference Time | Model Size |
|-------|-----------|----------|-----------|--------|----------------|------------|
| Model A | Isolation Forest | 82% | 0.79 | 0.85 | ~12ms | 12MB |
| Model B | Multinomial NB | 91% | 0.89 | 0.93 | ~8ms | 8MB |
| Model C | ORB+pHash | 76% | 0.88 | 0.71 | ~45ms* | 45MB |
| Model D | Weighted Ensemble | 87% | 0.91 | 0.84 | ~5ms | 2MB |

*Screenshot capture adds ~800ms (Playwright overhead)

**System Resource Usage:**
- RAM: 2.3GB (peak training), 400MB (inference mode)
- Disk: 180MB (compressed models), 2GB (SQLite + cache)
- CPU: Single-core optimized, zero GPU dependencies

---

## Academic Research Contributions

### CSC 405 - AI in Cybersecurity Capstone

1. **Unsupervised Zero-Day Detection**: Demonstrates that Isolation Forests trained exclusively on benign CommonCrawl data can generalize to novel phishing structures without retraining or labeled malicious datasets.

2. **Resource-Constrained ML**: Optimizes scikit-learn pipelines for sub-8GB RAM environments using:
   - Feature hashing (1024-dim)
   - Incremental learning (`partial_fit`)
   - Joblib compression (level 3)

3. **Multi-Modal Risk Fusion**: Proposes weighted ensemble method (URL 30%, Email 35%, Visual 35%) specifically calibrated for security contexts—precision-weighted to minimize false negatives.

---

## License

MIT License - See [LICENSE](https://opensource.org/licenses/MIT) for details.

---

## Acknowledgments

- **CommonCrawl** for providing benign URL datasets
- **Enron Dataset** for email training data
- **PhishTank** for real-time phishing intelligence
- **scikit-learn** team for excellent ML library

---

*PhantomSecDy Research Initiative | Detect the Undetectable*
