# PhishPulse v2.0

**Real-Time Multi-Modal Phishing Detection Engine**

*Hybrid Unsupervised Anomaly Detection + Supervised Forensic Analysis*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.103+-00a393.svg)](https://fastapi.tiangolo.com/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-f7931e.svg)](https://scikit-learn.org/)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-5+-646CFF.svg)](https://vitejs.dev/)

> **PhantomSecDy Research Initiative | Detect the Undetectable**

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Key Innovations](#key-innovations)
3. [System Architecture](#system-architecture)
4. [The Four AI Models](#the-four-ai-models)
   - [Model A: URL Lexical Analyzer](#model-a-url-lexical-analyzer-unsupervised)
   - [Model B: Email Forensic Analyzer](#model-b-email-forensic-analyzer-supervised)
   - [Model C: Visual Phishing Detector](#model-c-visual-phishing-detector-unsupervised)
   - [Model D: Risk Fusion Engine](#model-d-risk-fusion-engine-ensemble)
5. [Technology Stack](#technology-stack)
6. [Project Structure](#project-structure)
7. [Installation & Setup](#installation--setup)
8. [Training Pipeline](#training-pipeline)
9. [Running the System](#running-the-system)
10. [API Reference](#api-reference)
11. [Browser Extension](#browser-extension)
12. [React Dashboard](#react-dashboard)
13. [PDF Forensic Reporting](#pdf-forensic-reporting)
14. [Performance Benchmarks](#performance-benchmarks)
15. [Security Hardening](#security-hardening)
16. [Roadmap](#roadmap)
17. [License](#license)

---

## Executive Summary

PhishPulse is a production-grade, four-model ensemble cybersecurity framework engineered for real-time detection of phishing attacks across **URL**, **email**, and **visual** attack vectors. Architected specifically for resource-constrained environments, it employs unsupervised anomaly detection for zero-day threat discovery while leveraging supervised forensic analysis for known attack pattern recognition.

### What Makes PhishPulse Different

Unlike signature-based solutions or simple API wrappers that merely query threat databases, PhishPulse utilizes a **hybrid AI architecture** that operates entirely on-device. It trains Isolation Forests exclusively on benign data to detect novel structural anomalies without ever requiring labeled malicious datasets, while employing ORB computer vision and TF-IDF classification for specific attack vectors. This achieves **80-89% detection accuracy** with millisecond-level inference latency on CPU-only hardware.

### Core Capabilities

| Capability | Description |
|------------|-------------|
| **Real-Time URL Analysis** | Structural anomaly detection with entropy, Levenshtein distance, and suspicious TLD scoring |
| **Email Forensics** | SPF/DKIM/DMARC validation, header mismatch detection, and semantic urgency analysis |
| **Visual Phishing Detection** | Perceptual hashing and ORB feature matching against 200+ brand logos |
| **Risk Fusion** | Weighted ensemble with isotonic regression calibration for calibrated confidence intervals |
| **PDF Reporting** | 6-page forensic reports with MITRE ATT&CK mapping and IOC tables |
| **Browser Extension** | Cross-browser Manifest V3 extension for Gmail/Outlook integration |
| **React Dashboard** | Real-time threat monitoring with D3.js risk gauges and scan history |

---

## Key Innovations

### 1. Unsupervised Zero-Day Detection

PhishPulse demonstrates that Isolation Forests trained exclusively on benign CommonCrawl data can generalize to novel phishing structures without retraining or labeled malicious datasets. This is critical for detecting zero-day phishing campaigns that evade signature-based detection.

### 2. Resource-Constrained ML Optimization

Built for sub-8GB RAM environments using:
- **Feature hashing** (1024-dim HashingVectorizer) instead of full vocabulary matrices
- **Incremental learning** (`partial_fit`) for streaming email classification
- **Joblib compression** (level 3) keeping models under 50MB each
- **CPU-only inference** with zero GPU dependencies

### 3. Multi-Modal Risk Fusion

Proposes a weighted ensemble method (URL 30%, Email 35%, Visual 35%) specifically calibrated for security contexts—precision-weighted to minimize false negatives while maintaining acceptable false positive rates for production deployment.

### 4. Visual Brand Impersonation Detection

Uses ORB (Oriented FAST and Rotated BRIEF) keypoint detection combined with 64-bit perceptual hashing (pHash) to detect visual brand impersonation without requiring labeled phishing imagery—only legitimate brand logos are needed for the reference database.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              INPUT LAYER                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │   URL Scan   │  │ Email Scan   │  │ Visual Scan  │  │  Bulk Scan   │   │
│  │  (POST /scan)│  │ (POST /scan) │  │ (POST /scan) │  │ (POST /scan)│   │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘   │
└─────────┼─────────────────┼─────────────────┼─────────────────┼───────────┘
          │                 │                 │                 │
          └─────────────────┴─────────┬───────┴─────────────────┘
                                        │
                              ┌─────────▼─────────┐
                              │   FASTAPI ROUTER  │
                              │   (Orchestration) │
                              └─────────┬─────────┘
                                        │
          ┌─────────────────────────────┼─────────────────────────────┐
          │                             │                             │
          ▼                             ▼                             ▼
┌───────────────────┐    ┌───────────────────┐    ┌───────────────────┐
│   MODEL A         │    │   MODEL B         │    │   MODEL C         │
│   URL Lexical     │    │   Email Forensic  │    │   Visual Detector │
│   Analyzer        │    │   Analyzer        │    │                   │
│                   │    │                   │    │                   │
│  Isolation Forest │    │  Multinomial NB   │    │  ORB + pHash      │
│  + Regex Heuristics│   │  + TF-IDF         │    │  Perceptual Hash  │
│  + Entropy Calc   │    │  + Header Parser  │    │  + Form Detection │
│  + Levenshtein    │    │  + SPF/DKIM/DMARC │    │  + SSL Badge Spoof│
│  + TLD Scoring    │    │  + Urgency Keywords│   │  + Brand Matching │
└─────────┬─────────┘    └─────────┬─────────┘    └─────────┬─────────┘
          │                        │                        │
          │    url_risk_score      │    email_risk_score    │    visual_match
          │         (0-100)        │         (0-100)        │         (0-100)
          │                        │                        │
          └────────────────────────┼────────────────────────┘
                                   │
                         ┌─────────▼─────────┐
                         │   MODEL D         │
                         │   Risk Fusion     │
                         │   Engine          │
                         │                   │
                         │  Weighted Voting  │
                         │  Isotonic Regress │
                         │  Domain Age Check │
                         │  SSL Validation   │
                         └─────────┬─────────┘
                                   │
                         ┌─────────▼─────────┐
                         │   FINAL SCORE     │
                         │     (0-100)       │
                         └─────────┬─────────┘
                                   │
          ┌────────────────────────┼────────────────────────┐
          │                        │                        │
          ▼                        ▼                        ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  Classification  │  │  PDF Forensic    │  │  SQLite Storage  │
│  (Clean/           │  │  Report (6-page) │  │  (Scan History)  │
│   Suspicious/      │  │                  │  │                  │
│   Malicious/       │  │  - Threat Intel  │  │  - Scan metadata │
│   Critical)        │  │  - MITRE Mapping │  │  - Model scores  │
│                    │  │  - IOC Tables    │  │  - Timestamps    │
│  Color-coded:      │  │  - Screenshots   │  │  - Classifications│
│  Green/Amber/      │  │  - Remediation   │  │                  │
│  Red/Crimson       │  │                  │  │                  │
└──────────────────┘  └──────────────────┘  └──────────────────┘
```

---

## The Four AI Models

### Model A: URL Lexical Analyzer (Unsupervised)

**Algorithm:** Isolation Forest + Regex Heuristics  
**Type:** Unsupervised Anomaly Detection  
**Purpose:** Zero-day phishing detection via structural anomaly identification

#### Technical Implementation

| Feature | Description | Mathematical Basis |
|---------|-------------|-------------------|
| **Shannon Entropy** | Character-level randomness for DGA (Domain Generation Algorithm) detection | $H(X) = -\sum p(x) \log_2 p(x)$ |
| **Levenshtein Distance** | Dynamic programming string similarity to Alexa Top 1,000 domains | $O(m \times n)$ DP matrix |
| **Suspicious TLD** | Weighted risk matrix for high-abuse top-level domains | .tk +15, .ml +15, .xyz +10, .top +8 |
| **Subdomain Depth** | Excessive nesting detection (e.g., `login.secure.paypal.com.phish.com`) | Tree depth analysis |
| **URL Length** | Anomaly detection for unusually long obfuscated URLs | Z-score normalization |
| **Special Character Density** | Ratio of non-alphanumeric characters | Density threshold > 0.15 |
| **Brand Impersonation** | Regex pattern matching for known brand typosquatting | 110+ brand patterns |

#### Training Pipeline

```bash
python3 backend/training/train_url_analyzer.py \
    --benign-data data/commoncrawl_top100k.csv \
    --contamination 0.1 \
    --n-estimators 150 \
    --max-samples 0.8 \
    --output models/url_isolation_forest.pkl.gz
```

**Training Data:** 100,000 benign URLs from CommonCrawl WET files  
**Output:** `url_risk_score` (0-100), `brand_impersonated`, `structural_anomalies[]`

---

### Model B: Email Forensic Analyzer (Supervised)

**Algorithm:** TF-IDF + Multinomial Naive Bayes + Header Heuristics  
**Type:** Supervised Classification  
**Purpose:** Authentication protocol validation and semantic content analysis

#### Technical Implementation

| Feature | Description | Implementation |
|---------|-------------|----------------|
| **SPF Validation** | Sender Policy Framework DNS check | `dns.resolver.query` TXT record parsing |
| **DKIM Verification** | DomainKeys Identified Mail signature validation | Header `DKIM-Signature` parsing |
| **DMARC Alignment** | Domain-based Message Authentication alignment | `From` vs `DKIM-Signature` domain comparison |
| **Return-Path Analysis** | Header mismatch detection for spoofing indicators | `Return-Path` vs `From` domain comparison |
| **TF-IDF Vectorization** | Term frequency-inverse document frequency for content analysis | `HashingVectorizer(n_features=1024)` |
| **Urgency Keywords** | Detection of pressure tactics | "immediate action", "verify now", "account suspended", "limited time" |
| **HTML-to-Text Ratio** | Detection of image-heavy phishing emails | DOM parser text extraction |
| **Link Mismatch** | Anchor text vs href domain mismatch | BeautifulSoup href extraction |
| **Attachment Analysis** | Suspicious file extension detection | `.exe`, `.zip`, `.docm`, `.js` blacklisting |

#### Training Pipeline

```bash
python3 backend/training/train_email_model.py \
    --benign data/enron_emails.csv \
    --phishing data/phishing_emails.csv \
    --batch-size 500 \
    --n-features 1024 \
    --output models/email_naive_bayes.pkl.gz
```

**Training Data:** Enron Dataset (500,000 benign) + PhishingCorpus (5,000 malicious)  
**Output:** `email_risk_score` (0-100), `sender_authenticity`, `spf_status`, `dkim_status`, `dmarc_status`, `urgency_score`

---

### Model C: Visual Phishing Detector (Unsupervised)

**Algorithm:** ORB (Oriented FAST and Rotated BRIEF) + Perceptual Hashing (pHash)  
**Type:** Unsupervised Computer Vision  
**Purpose:** Visual brand impersonation detection without labeled phishing imagery

#### Technical Implementation

| Feature | Description | Implementation |
|---------|-------------|----------------|
| **ORB Features** | CPU-optimized keypoint detection and description | `cv2.ORB_create(nfeatures=500)` |
| **Perceptual Hashing** | 64-bit pHash with Hamming distance comparison | DCT-based hash generation |
| **Form Detection** | CV template matching for credential input fields | Contour analysis + HOG features |
| **SSL Badge Spoofing** | Template matching for fraudulent security icons | Multi-scale template matching |
| **Brand Logo Matching** | Hamming distance comparison against reference database | Threshold < 10 for match |
| **Screenshot Capture** | Headless browser page capture | Playwright Chromium automation |
| **DOM Structure Analysis** | Login form detection via HTML structure | BeautifulSoup form parsing |

#### Brand Database

The system maintains a reference database of 200+ legitimate brand logos including:
- Financial: PayPal, Chase, Bank of America, Wells Fargo, Citibank
- Technology: Apple, Google, Microsoft, Amazon, Meta
- Social: Facebook, Instagram, Twitter/X, LinkedIn, TikTok
- Enterprise: Salesforce, Workday, DocuSign, Dropbox

#### Training Pipeline

```bash
# Step 1: Download brand logo samples
python3 backend/training/train_visual.py --download-samples

# Step 2: Add custom brand logos to data/brand_logos/{brand_name}/

# Step 3: Generate perceptual hashes
python3 backend/training/train_visual.py \
    --brand-dir data/brand_logos/ \
    --orb-features 500 \
    --output models/visual_hashes.db
```

**Training Data:** No malicious images required—unsupervised matching against legitimate brand database only  
**Output:** `visual_match_confidence` (0-100), `impersonated_brand`, `form_detected`, `ssl_badge_spoofed`

---

### Model D: Risk Fusion Engine (Ensemble)

**Algorithm:** Weighted Voting + Isotonic Regression Calibration  
**Type:** Meta-Classifier Ensemble  
**Purpose:** Multi-modal signal aggregation with calibrated confidence intervals

#### Weight Distribution

| Model | Weight | Rationale |
|-------|--------|-----------|
| URL Analysis (Model A) | 30% | Structural anomalies are strong but not definitive indicators |
| Email Forensics (Model B) | 35% | Authentication failures provide high-confidence signals |
| Visual Detection (Model C) | 35% | Brand impersonation is a direct phishing indicator |

#### Calibration

Isotonic regression is applied to the weighted sum to produce calibrated probability estimates:

```python
from sklearn.isotonic import IsotonicRegression

calibrator = IsotonicRegression(out_of_bounds='clip')
calibrator.fit(weighted_scores, true_labels)
calibrated_score = calibrator.predict(weighted_score)
```

#### Risk Thresholds

| Score Range | Classification | Color | Action |
|-------------|----------------|-------|--------|
| 0-30 | Clean | Green | Safe to proceed |
| 31-60 | Suspicious | Amber | Caution advised, verify manually |
| 61-85 | Malicious | Red | Block immediately, investigate |
| 86-100 | Critical | Crimson | Critical threat, isolate and report |

#### Domain Age Penalty

Domains registered within the last 7 days receive an additional +20 risk points:

```python
if domain_age_days < 7:
    final_score = min(100, final_score + 20)
```

#### SSL Validation

Missing or invalid SSL certificates add +15 risk points:

```python
if not ssl_valid or ssl_expired:
    final_score = min(100, final_score + 15)
```

**Output:** `final_score` (0-100), `classification`, `confidence_interval` [lower, upper], `model_breakdown`, `indicators[]`, `mitigation_steps[]`

---

## Technology Stack

### Backend

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Framework | FastAPI | 0.103+ | Async REST API |
| ORM | SQLAlchemy | 2.0+ | Database abstraction |
| Database | SQLite | 3.39+ | WAL mode for concurrency |
| ML | scikit-learn | 1.3+ | Isolation Forest, Naive Bayes |
| CV | OpenCV (opencv-python) | 4.8+ | ORB, pHash, form detection |
| Screenshot | Playwright | 1.40+ | Headless browser capture |
| PDF | ReportLab | 3.6+ | Forensic report generation |
| DNS | dnspython | 2.4+ | SPF/DKIM/DMARC validation |
| HTTP | httpx | 0.25+ | Async HTTP client |
| Server | Uvicorn | 0.24+ | ASGI server |

### Frontend

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Framework | React | 18+ | UI components |
| Build Tool | Vite | 5+ | Fast development and bundling |
| Styling | Tailwind CSS | 3.4+ | Utility-first CSS |
| Charts | Recharts | 2.10+ | Risk gauges and statistics |
| HTTP Client | Axios | 1.6+ | API communication |
| Icons | Lucide React | 0.300+ | Consistent iconography |
| Routing | React Router | 6+ | SPA navigation |

### Browser Extension

| Component | Technology | Purpose |
|-----------|------------|---------|
| Manifest | Manifest V3 | Chrome/Firefox/Edge compatibility |
| Polyfill | webextension-polyfill | Cross-browser API unification |
| DOM Parsing | Vanilla JS | Gmail/Outlook content extraction |
| UI | HTML5 + CSS3 | Popup risk gauge interface |

### ML/AI Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Anomaly Detection | Isolation Forest | URL structural anomalies |
| Classification | Multinomial Naive Bayes | Email content classification |
| Feature Extraction | HashingVectorizer | Memory-efficient TF-IDF |
| Calibration | Isotonic Regression | Probability calibration |
| Computer Vision | ORB + pHash | Visual brand matching |
| Compression | joblib (level 3) | Model size optimization |

---

## Project Structure

```
phishpulse/
│
├── backend/                          # FastAPI Application
│   ├── app/
│   │   ├── main.py                   # FastAPI entry point, lifespan events
│   │   ├── config.py                 # Pydantic settings, model paths, thresholds
│   │   └── dependencies.py           # DB session injection, auth middleware
│   │
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── scan.py           # POST /scan (orchestrates all 4 models)
│   │       │   ├── report.py         # PDF generation, download endpoints
│   │       │   └── health.py         # System status, model versions, diagnostics
│   │       └── api.py                # Router aggregation and prefixing
│   │
│   ├── core/
│   │   ├── security.py               # CORS configuration, rate limiting (slowapi)
│   │   └── logging.py                # Structured JSON logging with context
│   │
│   ├── scanners/                     # The Four AI Model Implementations
│   │   ├── url_lexical.py            # Model A: Isolation Forest + regex heuristics
│   │   ├── email_forensics.py        # Model B: Naive Bayes + header analysis
│   │   ├── visual_detector.py        # Model C: ORB + pHash (OpenCV-based)
│   │   └── risk_fusion.py            # Model D: Weighted ensemble + isotonic regression
│   │
│   ├── services/
│   │   ├── pdf_generator.py          # 6-page forensic report engine (ReportLab)
│   │   ├── screenshot_service.py     # Playwright headless capture service
│   │   └── whois_lookup.py           # Domain intelligence and age calculation
│   │
│   ├── database/
│   │   ├── models.py                 # SQLAlchemy ORM schemas (Scan, Report, Settings)
│   │   ├── crud.py                   # Create, read, update, delete operations
│   │   └── session.py                # SQLite WAL mode, connection pooling
│   │
│   └── training/                     # Model Training & Validation
│       ├── train_url_analyzer.py     # Unsupervised Isolation Forest training
│       ├── train_email_model.py      # Supervised NB with incremental learning
│       ├── train_visual.py           # Brand logo hash generation and ORB feature extraction
│       └── validate_models.py        # Time-based split validation, stratified K-fold
│
├── extension/                        # Cross-Browser Extension (Manifest V3)
│   ├── manifest.json                 # Chrome/Firefox/Edge manifest
│   ├── background.js                 # Service worker for API communication
│   ├── content.js                    # Gmail/Outlook DOM extractors
│   ├── popup.html                    # Risk gauge popup UI
│   ├── popup.js                      # Extension logic and event handling
│   ├── styles.css                    # PhantomSecDy cyber aesthetic styling
│   └── lib/
│       └── browser-polyfill.js       # webextension-polyfill for cross-browser support
│
├── frontend/                         # React Admin Dashboard
│   ├── src/
│   │   ├── components/
│   │   │   ├── RiskGauge.jsx         # Animated radial risk gauge (Recharts)
│   │   │   ├── ScanHistory.jsx       # Paginated scan timeline with filters
│   │   │   ├── ThreatWave.jsx        # Animated threat activity visualization
│   │   │   ├── AICoreCard.jsx        # Model status cards with live indicators
│   │   │   ├── TerminalOverlay.jsx   # Cyberpunk terminal-style log display
│   │   │   └── Sidebar.jsx           # Navigation sidebar with route links
│   │   │
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx         # Real-time stats, threat wave, AI core status
│   │   │   ├── Inject.jsx            # URL/Email/Visual scan submission interface
│   │   │   ├── Reports.jsx           # PDF download manager with preview
│   │   │   ├── Dossiers.jsx          # Detailed scan history with filtering
│   │   │   └── Settings.jsx          # Threshold configuration, model toggles
│   │   │
│   │   ├── services/
│   │   │   └── api.js                # Axios client with interceptors and base URL
│   │   │
│   │   ├── App.jsx                   # Root component with routing
│   │   ├── main.jsx                  # React DOM entry point
│   │   └── index.css                 # Tailwind directives + custom cyber theme
│   │
│   ├── index.html                    # HTML entry point
│   ├── package.json                  # Dependencies and scripts
│   ├── vite.config.js                # Vite configuration with proxy
│   └── tailwind.config.js            # Tailwind theme customization
│
├── data/                             # Training datasets (gitignored)
│   ├── benign_urls/                  # CommonCrawl WET extracts
│   ├── phishing_urls/                # PhishTank/URLhaus feeds
│   ├── enron_emails/                 # Enron email corpus
│   ├── phishing_emails/            # PhishingCorpus dataset
│   └── brand_logos/                # 200+ legitimate brand logos
│
├── models/                           # Trained model binaries (gitignored)
│   ├── url_isolation_forest.pkl.gz
│   ├── email_naive_bayes.pkl.gz
│   └── visual_hashes.db
│
├── reports/                          # Generated PDF forensic reports (gitignored)
│   └── *.pdf
│
├── requirements.txt                  # Python dependencies with pinned versions
└── README.md                         # This documentation
```

---

## Installation & Setup

### Prerequisites

```bash
# Verify Python version (3.9+ required)
python3 --version

# Check available RAM (4GB+ recommended, 2GB minimum for inference)
free -h

# Check disk space (5GB+ recommended)
df -h

# Verify system architecture
uname -m  # x86_64 or aarch64
```

### Step 1: Clone Repository
https://github.com/ifedayoadebayo03/PHISHPULSE01.git
```bash
git clone https://github.com/ifedayoadebayo03/PHISHPULSE01.git
cd phishpulse
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate

# Verify activation
which python3  # Should show .../phishpulse/venv/bin/python3
```

### Step 3: Install Python Dependencies

```bash
# Install with no cache to save disk space
pip install --no-cache-dir -r requirements.txt
```

**Key Dependencies:**
```
fastapi==0.103.2
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
scikit-learn==1.3.2
pandas==2.1.3
numpy==1.26.2
opencv-python==4.8.1.78
playwright==1.40.0
reportlab==3.6.13
python-multipart==0.0.6
httpx==0.25.2
dnspython==2.4.2
python-whois==0.8.4
joblib==1.3.2
```

### Step 4: Install Playwright Browsers

```bash
playwright install chromium
```

### Step 5: Initialize Database

```bash
python3 -c "from backend.database.models import create_tables; create_tables()"
```

This creates `phishpulse.db` with WAL mode enabled for concurrent read/write access.

### Step 6: Verify Installation

```bash
# Test model imports
python3 -c "import backend.scanners.url_lexical; print('✓ Model A loadable')"
python3 -c "import backend.scanners.email_forensics; print('✓ Model B loadable')"
python3 -c "import backend.scanners.visual_detector; print('✓ Model C loadable')"
python3 -c "import backend.scanners.risk_fusion; print('✓ Model D loadable')"
```

### Step 7: Frontend Setup

```bash
cd frontend
npm install
```

---

## Training Pipeline

### Model A: URL Lexical Analyzer

```bash
cd ~/Desktop/demo/phishpulse
source venv/bin/activate

python3 backend/training/train_url_analyzer.py \
    --benign-data data/commoncrawl_top100k.csv \
    --contamination 0.1 \
    --n-estimators 150 \
    --max-samples 0.8 \
    --max-features 1.0 \
    --bootstrap False \
    --n-jobs -1 \
    --output models/url_isolation_forest.pkl.gz
```

**Parameters:**
- `contamination`: Expected proportion of anomalies (0.1 = 10%)
- `n-estimators`: Number of base estimators (trees)
- `max-samples`: Subsampling size for each tree
- `bootstrap`: Whether to use bootstrapping (False = exact sampling)

### Model B: Email Forensic Analyzer

```bash
python3 backend/training/train_email_model.py \
    --benign data/enron_emails.csv \
    --phishing data/phishing_emails.csv \
    --batch-size 500 \
    --n-features 1024 \
    --alpha 1.0 \
    --fit-prior True \
    --output models/email_naive_bayes.pkl.gz
```

**Parameters:**
- `batch-size`: Incremental learning batch size (RAM optimization)
- `n-features`: HashingVectorizer feature dimensions (1024 for memory efficiency)
- `alpha`: Laplace smoothing parameter
- `fit-prior`: Whether to learn class prior probabilities

### Model C: Visual Phishing Detector

```bash
# Step 1: Download sample brand logos
python3 backend/training/train_visual.py --download-samples

# Step 2: Organize brand logos
mkdir -p data/brand_logos
cp -r downloaded_logos/* data/brand_logos/

# Step 3: Generate hashes and train
python3 backend/training/train_visual.py \
    --brand-dir data/brand_logos/ \
    --orb-features 500 \
    --hash-size 64 \
    --output models/visual_hashes.db
```

### Model D: Risk Fusion Engine

The fusion engine does not require traditional training—it calibrates dynamically using isotonic regression on validation data:

```bash
python3 backend/training/validate_models.py \
    --url-model models/url_isolation_forest.pkl.gz \
    --email-model models/email_naive_bayes.pkl.gz \
    --visual-model models/visual_hashes.db \
    --validation-data data/validation_set.csv \
    --output models/fusion_calibrator.pkl
```

### Validation Strategy

| Validation Method | Purpose | Implementation |
|-------------------|---------|----------------|
| **Time-Based Split** | Prevent data leakage in temporal data | Train >30 days, test last 7 days |
| **Stratified K-Fold** | Maintain class distribution | k=5, stratified on classification |
| **Precision-Recall Focus** | Security context optimization | Minimize false negatives |
| **Cross-Validation** | Robust performance estimation | 5-fold with confidence intervals |

---

## Running the System

### 1. Start the Backend

```bash
cd ~/Desktop/demo/phishpulse
source venv/bin/activate

# Production mode (single worker due to RAM constraints)
uvicorn backend.app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 1 \
    --loop uvloop \
    --http h11

# Development mode with auto-reload
uvicorn backend.app.main:app \
    --reload \
    --port 8000 \
    --log-level debug
```

**Verify Backend:**
```bash
curl -s http://localhost:8000/api/v1/health/ | python3 -m json.tool
```

Expected response:
```json
{
    "status": "healthy",
    "version": "2.0.0",
    "models_loaded": {
        "url_analyzer": true,
        "email_forensics": true,
        "visual_detector": true,
        "risk_fusion": true
    },
    "database": "connected",
    "timestamp": "2026-06-25T22:54:00Z"
}
```

### 2. Start the Frontend

```bash
cd ~/Desktop/demo/phishpulse/frontend
npm run dev
```

The dashboard will be available at `http://localhost:5173`

### 3. Load Browser Extension

**Chrome/Edge:**
1. Navigate to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top-right)
3. Click "Load unpacked"
4. Select `~/Desktop/demo/phishpulse/extension/`
5. Configure API endpoint in popup settings: `http://localhost:8000`

**Firefox:**
1. Navigate to `about:debugging`
2. Click "This Firefox"
3. Click "Load Temporary Add-on"
4. Select `~/Desktop/demo/phishpulse/extension/manifest.json`

---

## API Reference

### Unified Scan Endpoint

```http
POST /api/v1/scan
Content-Type: application/json
```

**Request Body:**
```json
{
    "type": "url",
    "target": "http://paypa1-security-update.com/login",
    "options": {
        "screenshot": true,
        "generate_report": true,
        "whois_lookup": true
    }
}
```

**Scan Types:** `url`, `email`, `visual`, `bulk`

**Response:**
```json
{
    "scan_id": "550e8400-e29b-41d4-a716-446655440000",
    "timestamp": "2026-06-25T22:54:00Z",
    "scan_type": "url",
    "target": "http://paypa1-security-update.com/login",
    "final_score": 87,
    "classification": "Critical",
    "confidence_interval": [0.82, 0.91],
    "model_breakdown": {
        "url_analyzer": {
            "score": 85,
            "weight": 0.30,
            "details": {
                "entropy": 4.2,
                "levenshtein_distance": 2,
                "suspicious_tld": false,
                "subdomain_depth": 3,
                "brand_impersonated": "PayPal"
            }
        },
        "email_forensics": {
            "score": 0,
            "weight": 0.35,
            "details": {
                "note": "Not applicable for URL scan type"
            }
        },
        "visual_detector": {
            "score": 90,
            "weight": 0.35,
            "details": {
                "match_confidence": 0.94,
                "impersonated_brand": "PayPal",
                "form_detected": true,
                "ssl_badge_spoofed": true
            }
        }
    },
    "indicators": [
        "High Levenshtein distance from paypal.com (distance: 2)",
        "Domain registered 2 days ago (age: 2 days)",
        "Visual match: PayPal logo detected with 94% confidence",
        "Credential form detected on suspicious domain",
        "SSL badge spoofing detected"
    ],
    "mitigation_steps": [
        "Block domain at firewall immediately",
        "Reset credentials if submitted on this domain",
        "Submit URL to PhishTank API for community protection",
        "Notify security team of PayPal impersonation campaign"
    ],
    "whois_data": {
        "registrar": "NameCheap, Inc.",
        "creation_date": "2026-06-23T00:00:00Z",
        "expiration_date": "2027-06-23T00:00:00Z",
        "name_servers": ["ns1.cloudflare.com", "ns2.cloudflare.com"],
        "privacy_protected": true
    },
    "report_url": "/api/v1/reports/download/550e8400-e29b-41d4-a716-446655440000.pdf",
    "processing_time_ms": 1247
}
```

### Email Scan Endpoint

```http
POST /api/v1/scan
Content-Type: application/json
```

```json
{
    "type": "email",
    "target": "raw_email_content_here",
    "options": {
        "parse_headers": true,
        "check_spf_dkim_dmarc": true,
        "analyze_attachments": true
    }
}
```

### Visual Scan Endpoint

```http
POST /api/v1/scan
Content-Type: application/json
```

```json
{
    "type": "visual",
    "target": "https://suspicious-bank-login.com",
    "options": {
        "capture_screenshot": true,
        "compare_brands": ["Chase", "Bank of America", "Wells Fargo"],
        "detect_forms": true
    }
}
```

### Health Check Endpoints

```http
GET /api/v1/health/
```

Returns system status, database connectivity, and model load status.

```http
GET /api/v1/health/detail
```

Returns detailed diagnostics including:
- Model version information
- Last training timestamps
- Memory usage statistics
- Database size and record counts
- Average response times

```http
GET /api/v1/health/model-info
```

Returns metadata for all loaded models:
- Algorithm types
- Training data sources
- Feature dimensions
- Accuracy metrics from validation
- Model file sizes

### Report Endpoints

```http
GET /api/v1/reports/download/{scan_id}.pdf
```

Downloads the forensic PDF report for a specific scan.

```http
GET /api/v1/reports/list
```

Lists all generated reports with metadata (filename, scan_id, timestamp, file_size).

### Scan History

```http
GET /api/v1/scan/history?page=1&limit=20&classification=Critical
```

Paginated scan history with filtering by classification, date range, and scan type.

---

## Browser Extension

### Supported Platforms

| Browser | Version | Status |
|---------|---------|--------|
| Google Chrome | 88+ | Fully supported |
| Mozilla Firefox | 85+ | Fully supported |
| Microsoft Edge | 88+ | Fully supported |
| Brave | 1.20+ | Fully supported |
| Opera | 74+ | Compatible |

### Supported Email Platforms

| Platform | Selector Strategy | Status |
|----------|-------------------|--------|
| Gmail | `div[role="listitem"]` | Active |
| Outlook Live | `div[data-conversation-id]` | Active |
| Outlook 365 | `div[id*="UniqueBody"]` | Active |
| Hotmail | `.ReadMsgBody` | Active |
| Yahoo Mail | `.email-pannable` | Beta |

### Extension Features

1. **Real-Time Risk Indicators**: Injects color-coded risk badges next to links in emails
2. **Popup Risk Gauge**: Click extension icon to see current page risk score
3. **Context Menu Scan**: Right-click any link → "Scan with PhishPulse"
4. **Auto-Scan**: Automatically scans links on page load (configurable)
5. **Dashboard Link**: Quick access to React admin dashboard

### Extension Permissions

```json
{
    "permissions": [
        "activeTab",
        "storage",
        "background",
        "contextMenus"
    ],
    "host_permissions": [
        "http://localhost:8000/*",
        "https://mail.google.com/*",
        "https://outlook.live.com/*",
        "https://outlook.office.com/*"
    ]
}
```

---

## React Dashboard

### Dashboard Page (`/`)

- **Threat Wave**: Animated visualization of recent scan activity
- **AI Core Cards**: Live status of all four models with load indicators
- **Risk Gauge**: Real-time system-wide risk summary
- **Terminal Overlay**: Cyberpunk-style log stream from backend
- **Quick Stats**: Total scans, threat detections, average response time

### Inject Page (`/inject`)

- **URL Scanner**: Single URL input with options toggle
- **Email Scanner**: Paste raw email content with header analysis
- **Visual Scanner**: Submit URL for screenshot and visual analysis
- **Bulk Scanner**: Upload CSV file for batch processing
- **Terminal UI**: Real-time scan progress with model-by-model breakdown

### Reports Page (`/reports`)

- **Report List**: All generated PDFs with download links
- **Preview Panel**: Inline PDF preview (browser-supported)
- **Filter Controls**: Date range, classification, scan type
- **Batch Download**: Select multiple reports for zip download

### Dossiers Page (`/dossiers`)

- **Scan History**: Complete chronological scan log
- **Detail View**: Expand any scan for full model breakdown
- **Search**: Full-text search across indicators and targets
- **Export**: CSV export of filtered results

### Settings Page (`/settings`)

- **Threshold Sliders**: Adjust risk classification boundaries
- **Model Toggles**: Enable/disable individual models
- **Weight Configuration**: Adjust Model D fusion weights
- **API Configuration**: Backend URL and timeout settings
- **Theme Toggle**: Dark/Light mode (default: dark cyber)

---

## PDF Forensic Reporting

### Report Structure (6 Pages)

| Page | Content | Visual Elements |
|------|---------|----------------|
| **1. Executive Cover** | Risk score, classification, timestamp, target | Risk gauge, color banner, QR code |
| **2. Threat Intelligence** | MITRE ATT&CK mapping, IOC tables, threat actor attribution | Matrix diagram, IOC table |
| **3. Technical Forensics** | URL decomposition, WHOIS data, email header analysis | Tree diagram, header table |
| **4. Visual Evidence** | Screenshots, side-by-side brand comparison, form detection | Image gallery, comparison panels |
| **5. AI Model Analysis** | Feature importance, model consensus, confidence intervals | Bar charts, radar chart |
| **6. Remediation & Compliance** | Action checklist, GDPR Article 33, PCI-DSS mapping | Checklist, compliance matrix |

### Design System

- **Headers**: Navy blue (#1a237e) with white text
- **Warnings**: Amber (#ff8f00) for Suspicious classifications
- **Critical**: Crimson (#c62828) for Malicious/Critical classifications
- **Clean**: Green (#2e7d32) for Clean classifications
- **Fonts**: Helvetica (body), Times New Roman (headers), Courier (code/logs)
- **Layout**: Professional academic + corporate hybrid aesthetic

### Sample Report Generation

```bash
curl -X POST http://localhost:8000/api/v1/scan \
    -H "Content-Type: application/json" \
    -d '{
        "type": "url",
        "target": "http://suspicious-example.com/login",
        "options": {
            "generate_report": true
        }
    }'
```

Report saved to: `reports/{scan_id}.pdf`

---

## Performance Benchmarks

### Model Performance

| Model | Algorithm | Accuracy | Precision | Recall | F1-Score | Inference Time | Model Size |
|-------|-----------|----------|-----------|--------|----------|----------------|------------|
| Model A | Isolation Forest | 82% | 0.79 | 0.85 | 0.82 | ~12ms | 12MB |
| Model B | Multinomial NB | 91% | 0.89 | 0.93 | 0.91 | ~8ms | 8MB |
| Model C | ORB + pHash | 76% | 0.88 | 0.71 | 0.79 | ~45ms* | 45MB |
| Model D | Weighted Ensemble | 87% | 0.91 | 0.84 | 0.87 | ~5ms | 2MB |

*Screenshot capture adds ~800ms (Playwright headless browser overhead)

### System Resource Usage

| Resource | Training Peak | Inference Mode | Idle |
|----------|---------------|----------------|------|
| **RAM** | 2.3GB | 400MB | 180MB |
| **Disk** | 2.5GB (models + data) | 180MB (compressed models) | 50MB |
| **CPU** | Multi-core (training) | Single-core optimized | Near-zero |
| **GPU** | None required | None required | None required |

### Throughput

| Endpoint | Requests/sec | Avg Latency | Max Payload |
|----------|-------------|-------------|-------------|
| URL Scan | 45 | 15ms | 2KB |
| Email Scan | 30 | 25ms | 500KB |
| Visual Scan | 5 | 1200ms | 5MB |
| Bulk Scan | 10 | 500ms | 1MB |
| PDF Report | 2 | 3000ms | 10MB |

### Scalability Notes

- Single-worker Uvicorn recommended for <8GB RAM systems
- SQLite WAL mode supports concurrent reads during writes
- Model loading is lazy—only loaded on first scan request
- Joblib memory mapping reduces RAM duplication across requests

---

## Security Hardening

### CORS Configuration

```python
# backend/core/security.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "chrome-extension://*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
    max_age=3600,
)
```

### Rate Limiting

```python
# Using slowapi with Redis backend (or in-memory for single-instance)
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/v1/scan")
@limiter.limit("30/minute")
async def scan_endpoint(request: Request, ...):
    ...
```

### Input Validation

- URL validation with `pydantic.HttpUrl`
- Email content size limit: 10MB
- Screenshot timeout: 30 seconds max
- SQL injection prevention via SQLAlchemy ORM
- XSS prevention via output encoding in frontend

### Data Protection

- Scan logs purged after 90 days (configurable)
- Email content processed in-memory, never persisted raw
- WHOIS data cached for 24 hours to reduce external queries
- PDF reports include watermark with generation timestamp

---

## Roadmap

### Completed

- [x] Model A: URL Lexical Analyzer (Isolation Forest)
- [x] Model B: Email Forensic Analyzer (Naive Bayes + Headers)
- [x] Model C: Visual Phishing Detector (ORB + pHash)
- [x] Model D: Risk Fusion Engine (Weighted Ensemble)
- [x] FastAPI Backend with SQLite WAL
- [x] React Dashboard with Vite + Tailwind
- [x] Cross-Browser Extension (Manifest V3)
- [x] 6-Page PDF Forensic Reporting
- [x] Training Pipelines with Incremental Learning
- [x] Resource-Constrained Optimization (<8GB RAM)

### In Progress

- [ ] Browser extension Firefox AMO submission
- [ ] Chrome Web Store publication
- [ ] Model compression with ONNX Runtime
- [ ] Docker containerization
- [ ] CI/CD pipeline with GitHub Actions

### Planned

- [ ] Real-time PhishTank API integration for threat feeds
- [ ] Machine learning model versioning with MLflow
- [ ] Distributed scanning with Celery + Redis
- [ ] PostgreSQL migration for production scale
- [ ] Kubernetes deployment manifests
- [ ] Grafana + Prometheus monitoring stack
- [ ] Mobile app (React Native) for on-the-go scanning
- [ ] QR code phishing detection module

---

## License

MIT License

Copyright (c) 2026 PhantomSecDy Research Initiative

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## Acknowledgments

- **CommonCrawl** for providing open-access benign URL datasets from web crawls
- **Enron Dataset** for the foundational email corpus used in academic research
- **PhishTank** community for real-time phishing intelligence and verification
- **PhishingCorpus** for curated malicious email samples
- **scikit-learn** team for the excellent machine learning library and documentation
- **FastAPI** team for the high-performance async web framework
- **OpenCV** community for computer vision algorithms and optimizations
- **ReportLab** team for the PDF generation toolkit

---

## Contact & Support

**Project:** PhishPulse v2.0  
**Organization:** PhantomSecDy Research Initiative  
**Repository:** https://github.com/ifedayoadebayo03/PHISHPULSE01.git


For bug reports, feature requests, or security disclosures, please open an issue on the GitHub repository.

---

*PhantomSecDy Research Initiative | Detect the Undetectable*

*Built with precision. Engineered for defense. Deployed with confidence.*
