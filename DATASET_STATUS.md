# PhishPulse Dataset Download Summary

## ✅ Downloaded Datasets (All Models)

### Model A: URL Lexical Analyzer
| Dataset | File | Size | Records | Status |
|---------|------|------|---------|--------|
| Majestic Million | `data/urls/majestic_million.csv` | 77 MB | 1,000,000 URLs | ✅ READY |

**Anonymity**: Public domain ranking data - no personal information

### Model B: Email Forensic Analyzer
| Dataset | File | Size | Records | Status |
|---------|------|------|---------|--------|
| Enron-Spam | `data/emails/enron_spam_data.csv` | 50 MB | 33,716 emails | ✅ READY |
| Full Enron | `data/emails/enron_mail.tar.gz` | ~63 MB (downloading) | 500,000 emails | ⏳ IN PROGRESS |

**Anonymity**: 
- Enron-Spam: Pre-processed, anonymized dataset
- Full Enron: Public domain federal evidence, already anonymized

### Model C: Visual Phishing Detector
| Dataset | Location | Brands | Images | Status |
|---------|----------|--------|--------|--------|
| Brand Logos | `data/brand_logos/` | 20 brands | 20+ logos | ✅ READY |

**Brands Included**: paypal, microsoft, google, apple, amazon, facebook, netflix, linkedin, dropbox, adobe, twitter, instagram, github, spotify, slack, zoom, salesforce, oracle, ibm, intel

**Anonymity**: Public company logos - no personal data

---

## 🚀 How to Train Models

### Model A (URL Analyzer)
```bash
python3 backend/training/train_url_analyzer.py \
    --benign-data data/urls/majestic_million.csv \
    --contamination 0.1 \
    --output models/url_isolation_forest.pkl.gz
```

### Model B (Email Analyzer)
```bash
# Using Enron-Spam (ready now)
python3 backend/training/train_email_model.py \
    --data data/emails/enron_spam_data.csv \
    --output models/email_nb_model.pkl

# Or wait for full Enron to complete downloading
```

### Model C (Visual Detector)
```bash
python3 backend/training/train_visual.py \
    --brand-dir data/brand_logos/ \
    --output models/visual_hashes.db
```

---

## 📁 Data Directory Structure

```
phishpulse/data/
├── urls/
│   └── majestic_million.csv          (1M URLs)
├── emails/
│   ├── enron_spam_data.csv           (33k labeled emails)
│   └── enron_mail.tar.gz             (500k emails - downloading)
└── brand_logos/
    ├── paypal/paypal_logo.ico
    ├── microsoft/microsoft_logo.ico
    ├── google/google_logo.ico
    ├── apple/apple_logo.ico
    ├── amazon/amazon_logo.ico
    ├── facebook/facebook_logo.ico
    ├── netflix/netflix_logo.ico
    ├── linkedin/linkedin_logo.ico
    ├── dropbox/dropbox_logo.png
    ├── adobe/adobe_logo.ico
    ├── twitter/twitter_logo.ico
    ├── instagram/instagram_logo.ico
    ├── github/github_logo.ico
    ├── spotify/spotify_logo.ico
    ├── slack/slack_logo.ico
    ├── zoom/zoom_logo.ico
    ├── salesforce/salesforce_logo.ico
    ├── oracle/oracle_logo.ico
    ├── ibm/ibm_logo.ico
    └── intel/intel_logo.ico
```

---

## 🔒 Anonymity & Privacy Notes

All datasets used are:
1. **Public Domain** or **Open Source**
2. **Already anonymized** by original providers
3. **No personally identifiable information (PII)**
4. **Cannot be traced back** to individuals
5. **Commonly used** in academic research

### Dataset Sources:
- **Majestic Million**: Public web ranking by Majestic SEO
- **Enron**: Public domain federal evidence (CMU)
- **Brand Logos**: Public company favicons and icons

---

## ⏳ Background Process

The full Enron dataset (1.5GB) is still downloading in the background.
- Current progress: ~13% (63MB downloaded)
- Estimated time: ~40 minutes remaining
- Process ID: Check with `ps aux | grep enron`

You can start training Model A and Model C immediately.
Model B can use Enron-Spam (ready now) or wait for full Enron.
