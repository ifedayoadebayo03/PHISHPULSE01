# PhishPulse Training Datasets Guide

This guide provides comprehensive information on acquiring datasets for training PhishPulse's four AI models.

## Table of Contents
1. [Model A: URL Lexical Analyzer](#model-a-url-lexical-analyzer)
2. [Model B: Email Forensic Analyzer](#model-b-email-forensic-analyzer)
3. [Model C: Visual Phishing Detector](#model-c-visual-phishing-detector)
4. [Quick Download Scripts](#quick-download-scripts)

---

## Model A: URL Lexical Analyzer

### Training Data Requirements
- **Type**: Unsupervised (benign URLs only)
- **Volume**: 100k+ benign URLs
- **Format**: CSV or text file (one URL per line)

### Dataset Sources

#### 1. CommonCrawl WET Files (Primary Source)
**Description**: Web crawl data containing extracted text and URLs from billions of web pages.

**Download Options**:
- **Official**: https://commoncrawl.org/the-data/get-started/
- **AWS S3**: `s3://commoncrawl/`
- **Sample (Kaggle)**: https://www.kaggle.com/datasets/jyesawtellrickson/commoncrawl

**How to Extract URLs**:
```bash
# Install common crawl tools
pip install warcio

# Download a WET file segment
wget https://data.commoncrawl.org/crawl-data/CC-MAIN-2024-10/segments/1711832429398.42/wet/CC-MAIN-20240324165844-20240324195844-00000.warc.wet.gz

# Extract URLs
gunzip -c CC-MAIN-20240324165844-20240324195844-00000.warc.wet.gz | \
  grep -oP 'https?://[^\s<>"{}|\\^`\[\]]+' | \
  head -100000 > commoncrawl_top100k.csv
```

#### 2. Majestic Million (Alternative)
**Description**: Top 1 million websites ranked by Majestic SEO.

**Download**: https://majestic.com/reports/majestic-million

```bash
wget https://downloads.majestic.com/majestic_million.csv
# Extract URLs, skip header
tail -n +2 majestic_million.csv | cut -d',' -f3 | head -100000 > majestic_top100k.csv
```

#### 3. Cisco Umbrella Popularity List
**Description**: Most popular domains based on DNS queries.

**Download**: http://s3-us-west-1.amazonaws.com/umbrella-static/top-1m.csv.zip

```bash
wget http://s3-us-west-1.amazonaws.com/umbrella-static/top-1m.csv.zip
unzip top-1m.csv.zip
# Format as URLs
awk -F',' '{print "https://" $2}' top-1m.csv | head -100000 > umbrella_top100k.csv
```

#### 4. PhishTank (Validation Only - NOT for training Model A)
**Description**: Community-reported phishing URLs (use only for validation, NOT training).

**Download**: https://phishtank.org/developer_info.php

```bash
# Get API key from https://phishtank.org/api_info.php
wget http://data.phishtank.com/data/online-valid.json.gz
gunzip online-valid.json.gz
# Extract phishing URLs (for validation only)
python3 -c "import json; data=json.load(open('online-valid.json')); [print(u['url']) for u in data]" > phishing_urls.csv
```

---

## Model B: Email Forensic Analyzer

### Training Data Requirements
- **Type**: Supervised (benign + phishing emails)
- **Volume**: 500k benign + 5k phishing emails
- **Format**: CSV with columns: `text`, `label` (0=benign, 1=phishing)

### Dataset Sources

#### 1. Enron Email Dataset (Benign - Primary Source)
**Description**: ~500,000 emails from Enron employees (legitimate business emails).

**Download Options**:
- **Kaggle**: https://www.kaggle.com/datasets/wcukierski/enron-email-dataset
- **CMU**: https://www.cs.cmu.edu/~enron/
- **Direct**: http://www.cs.cmu.edu/~enron/enron_mail_20150507.tar.gz

**Preprocessing Script**:
```python
import pandas as pd
import os
import email
import glob

def parse_enron_emails(enron_dir, output_file, max_emails=500000):
    """Parse Enron emails into CSV format."""
    emails = []
    count = 0
    
    for root, dirs, files in os.walk(enron_dir):
        for file in files:
            if count >= max_emails:
                break
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    msg = email.message_from_file(f)
                    
                    # Extract text content
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            if content_type == "text/plain":
                                body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                                break
                    else:
                        body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
                    
                    subject = msg.get('Subject', '')
                    full_text = f"Subject: {subject}\n\n{body}"
                    
                    emails.append({'text': full_text, 'label': 0})
                    count += 1
                    
                    if count % 10000 == 0:
                        print(f"Processed {count} emails...")
            except Exception as e:
                continue
    
    df = pd.DataFrame(emails)
    df.to_csv(output_file, index=False)
    print(f"Saved {len(df)} emails to {output_file}")

# Usage
# parse_enron_emails('enron_mail_20150507/maildir/', 'enron_emails.csv')
```

#### 2. Enron-Spam Dataset (Pre-labeled)
**Description**: 33,716 emails (16,545 ham + 17,171 spam) - pre-labeled.

**Download**: https://www.kaggle.com/datasets/marcelwiechmann/enron-spam-data

```bash
# Direct download
wget https://raw.githubusercontent.com/MWiechmann/enron_spam_data/master/enron_spam_data.zip
unzip enron_spam_data.zip
```

#### 3. PhishingCorpus (Phishing Emails)
**Description**: Collection of phishing emails for training.

**Sources**:
- **PhishingCorpus**: https://monkey.org/~jose/phishing/
- **CSDMC2010 SPAM corpus**: http://csmining.org/index.php/spam-email-datasets.html

#### 4. Ling-Spam Dataset
**Description**: 2,893 emails (legitimate + spam).

**Download**: https://www.kaggle.com/datasets/venky73/spam-mails-dataset

**Direct**: http://www.aueb.gr/users/ion/data/lingspam_public.tar.gz

```bash
wget http://www.aueb.gr/users/ion/data/lingspam_public.tar.gz
tar -xzf lingspam_public.tar.gz
```

#### 5. 419 Nigerian Fraud Email Dataset
**Description**: Collection of advance-fee fraud emails.

**Download**: https://www.kaggle.com/datasets/rtatman/fraudulent-email-corpus

---

## Model C: Visual Phishing Detector

### Training Data Requirements
- **Type**: Unsupervised (brand logos only - legitimate)
- **Volume**: 200+ brand logos across 10+ categories
- **Format**: PNG/JPG images organized in folders

### Directory Structure
```
data/brand_logos/
├── paypal/
│   ├── logo.png
│   ├── icon.png
│   └── checkout_logo.png
├── microsoft/
│   ├── logo.png
│   ├── outlook_logo.png
│   └── office_logo.png
├── google/
│   ├── logo.png
│   ├── gmail_logo.png
│   └── drive_logo.png
└── ... (more brands)
```

### Dataset Sources

#### 1. Brand Logos Dataset (Recommended)
**World Brand Logos**: https://www.kaggle.com/datasets/lykinst/brand-logos

```bash
# Download from Kaggle
kaggle datasets download -d lykinst/brand-logos
unzip brand-logos.zip -d data/brand_logos/
```

#### 2. Logo-2K+ Dataset
**Description**: 2,000+ logo images across 10 categories.

**Download**: https://github.com/msubhransu/logo-2k-plus

#### 3. Flickr Logos 27 Dataset
**Description**: 27 logo classes with bounding boxes.

**Download**: http://image.ntua.gr/iva/datasets/flickr_logos/

#### 4. WebLogo-2M Dataset
**Description**: Large-scale logo dataset.

**Download**: https://github.com/ckcraig01/WEBLOGO-2M-Dataset

#### 5. Manual Collection Script
```python
import requests
from bs4 import BeautifulSoup
import os

def download_logo(brand_name, url, output_dir):
    """Download logo from URL."""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            ext = url.split('.')[-1].split('?')[0]
            if ext not in ['png', 'jpg', 'jpeg']:
                ext = 'png'
            filepath = os.path.join(output_dir, f"{brand_name}_logo.{ext}")
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {filepath}")
            return True
    except Exception as e:
        print(f"Error downloading {brand_name}: {e}")
    return False

# Popular brand logos (official sources)
BRAND_LOGOS = {
    "paypal": "https://www.paypal.com/paypalme/img/favicon.ico",
    "microsoft": "https://www.microsoft.com/favicon.ico",
    "google": "https://www.google.com/favicon.ico",
    "apple": "https://www.apple.com/favicon.ico",
    "amazon": "https://www.amazon.com/favicon.ico",
    "facebook": "https://www.facebook.com/favicon.ico",
    "netflix": "https://www.netflix.com/favicon.ico",
    "linkedin": "https://www.linkedin.com/favicon.ico",
    "dropbox": "https://www.dropbox.com/favicon.ico",
    "adobe": "https://www.adobe.com/favicon.ico",
}

os.makedirs("data/brand_logos", exist_ok=True)
for brand, url in BRAND_LOGOS.items():
    brand_dir = f"data/brand_logos/{brand}"
    os.makedirs(brand_dir, exist_ok=True)
    download_logo(brand, url, brand_dir)
```

---

## Quick Download Scripts

### Automated Setup Script

```bash
#!/bin/bash
# setup_datasets.sh - Automated dataset download script

set -e

echo "=== PhishPulse Dataset Setup ==="
mkdir -p data/{urls,emails,brand_logos}

# 1. Download CommonCrawl sample URLs (10k)
echo "[1/5] Downloading CommonCrawl sample URLs..."
if [ ! -f data/urls/commoncrawl_sample_10k.csv ]; then
    wget -q https://raw.githubusercontent.com/commoncrawl/cc-examples/main/url/samples/top-10k.txt \
        -O data/urls/commoncrawl_sample_10k.csv || \
        echo "Failed to download CommonCrawl sample. Please download manually."
fi

# 2. Download Majestic Million Top 100k
echo "[2/5] Downloading Majestic Million..."
if [ ! -f data/urls/majestic_million.csv ]; then
    wget -q https://downloads.majestic.com/majestic_million.csv \
        -O data/urls/majestic_million.csv || \
        echo "Failed to download Majestic Million. Please download manually."
fi

# 3. Download PhishTank (for validation only)
echo "[3/5] Downloading PhishTank data..."
if [ ! -f data/urls/phishtank.json ]; then
    wget -q http://data.phishtank.com/data/online-valid.json.gz \
        -O data/urls/phishtank.json.gz || \
        echo "Failed to download PhishTank. You may need an API key."
    if [ -f data/urls/phishtank.json.gz ]; then
        gunzip data/urls/phishtank.json.gz
    fi
fi

# 4. Download Enron-Spam
echo "[4/5] Downloading Enron-Spam dataset..."
if [ ! -f data/emails/enron_spam_data.csv ]; then
    wget -q "https://raw.githubusercontent.com/MWiechmann/enron_spam_data/master/enron_spam_data.zip" \
        -O data/emails/enron_spam_data.zip || \
        echo "Failed to download Enron-Spam. Please download manually from Kaggle."
    if [ -f data/emails/enron_spam_data.zip ]; then
        unzip -q data/emails/enron_spam_data.csv -d data/emails/
    fi
fi

# 5. Create brand logos directory structure
echo "[5/5] Setting up brand logos directory..."
mkdir -p data/brand_logos/{paypal,microsoft,google,apple,amazon,facebook,netflix,linkedin,dropbox,adobe}
echo "Brand logos directory created. Please add logo images manually."

echo "=== Dataset Setup Complete ==="
echo ""
echo "Next steps:"
echo "1. Check data/ directory for downloaded files"
echo "2. Add brand logos to data/brand_logos/{brand}/ directories"
echo "3. Run training scripts:"
echo "   python3 backend/training/train_url_analyzer.py --benign-data data/urls/commoncrawl_sample_10k.csv"
echo "   python3 backend/training/train_email_model.py --benign data/emails/enron_emails.csv --phishing data/emails/phishing_emails.csv"
echo "   python3 backend/training/train_visual.py --brand-dir data/brand_logos/"
```

---

## Data Preprocessing

### URL Preprocessing
```python
import pandas as pd
import validators

def clean_urls(input_file, output_file):
    """Clean and validate URLs."""
    with open(input_file, 'r') as f:
        urls = [line.strip() for line in f]
    
    # Validate and deduplicate
    valid_urls = []
    seen = set()
    
    for url in urls:
        if url in seen:
            continue
        if validators.url(url):
            valid_urls.append(url)
            seen.add(url)
    
    with open(output_file, 'w') as f:
        for url in valid_urls:
            f.write(url + '\n')
    
    print(f"Valid URLs: {len(valid_urls)} / {len(urls)}")

# Usage
# clean_urls('raw_urls.csv', 'clean_urls.csv')
```

### Email Preprocessing
```python
import pandas as pd
import re

def clean_emails(input_file, output_file):
    """Clean email dataset."""
    df = pd.read_csv(input_file)
    
    # Remove empty texts
    df = df.dropna(subset=['text'])
    
    # Remove very short emails (< 50 chars)
    df = df[df['text'].str.len() > 50]
    
    # Remove duplicates
    df = df.drop_duplicates(subset=['text'])
    
    # Clean text
    df['text'] = df['text'].apply(lambda x: re.sub(r'\s+', ' ', str(x)).strip())
    
    df.to_csv(output_file, index=False)
    print(f"Cleaned emails: {len(df)}")

# Usage
# clean_emails('raw_emails.csv', 'clean_emails.csv')
```

---

## Dataset Statistics

| Model | Dataset | Size | Records | Format |
|-------|---------|------|---------|--------|
| A | CommonCrawl | ~5GB | 100k URLs | CSV |
| A | Majestic Million | ~20MB | 1M URLs | CSV |
| B | Enron | ~1.5GB | 500k emails | CSV |
| B | Enron-Spam | ~85MB | 33k emails | CSV |
| B | PhishingCorpus | ~5MB | 5k emails | TXT |
| B | Ling-Spam | ~10MB | 2.9k emails | TXT |
| C | Logo-2K+ | ~500MB | 2k images | JPG/PNG |
| C | WebLogo-2M | ~10GB | 2M images | JPG/PNG |

---

## License & Attribution

### CommonCrawl
- License: CC0 (Public Domain)
- Citation: "Common Crawl Foundation. Common Crawl. https://commoncrawl.org"

### Enron
- License: Public Domain (federal evidence)
- Citation: "Cohen, William W. Enron Email Dataset. Carnegie Mellon University."

### PhishTank
- License: Creative Commons Attribution-ShareAlike 3.0
- Citation: "PhishTank. OpenDNS. https://phishtank.org"

### Majestic Million
- License: Free for non-commercial use
- Citation: "Majestic SEO. Majestic Million. https://majestic.com"

---

## Troubleshooting

### Common Issues

**Issue**: `wget` fails with certificate error  
**Solution**: Use `curl -L` instead or add `--no-check-certificate` (not recommended for production)

**Issue**: PhishTank download requires authentication  
**Solution**: Register for free API key at https://phishtank.org/api_info.php

**Issue**: Kaggle datasets require authentication  
**Solution**: Install Kaggle CLI: `pip install kaggle` and configure API key

**Issue**: Enron dataset too large  
**Solution**: Use Enron-Spam subset (33k emails) instead of full Enron (500k)

---

## Alternative Data Sources

### Commercial/Enterprise Options
1. **URLVoid**: https://www.urlvoid.com/api/ (API for URL reputation)
2. **VirusTotal**: https://www.virustotal.com/gui/join-us (Malware/URL database)
3. **Alexa Top Sites**: https://docs.aws.amazon.com/AlexaTopSites/ (AWS paid service)

### Academic Datasets
1. **CIC phishing dataset**: https://www.unb.ca/cic/datasets/phishing.html
2. **ISCX-URL-2016**: https://www.unb.ca/cic/datasets/url-2016.html
3. **PhishStorm**: https://data.mendeley.com/datasets/h3cgnj8hft/1

---

For additional assistance, please open an issue at: https://github.com/phantomsecdy/phishpulse/issues
