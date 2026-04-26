# Prompt for Kimi: Create Thesis Figures for PhishPulse Chapters 1-3

## Instructions for Kimi

When writing Chapters 1-3 of the PhishPulse thesis, **CREATE AND INSERT the following figures at the specified locations**. Each figure should include:
1. **Figure Number** (e.g., Figure 1.1, Figure 3.2)
2. **Caption** (descriptive title below the figure)
3. **Visual Content** (ASCII art, diagram description, or code to generate)
4. **In-text Reference** (sentence in the text that refers to the figure)

---

## CHAPTER 1: INTRODUCTION FIGURES

### Figure 1.1: The Phishing Attack Landscape
**Placement**: Section 1.1 (Background of the Study) - AFTER paragraph 2, BEFORE the paragraph on current techniques

**Description**: A diagram showing the three main types of phishing attacks that PhishPulse detects:
- URL-based (typosquatting, deceptive domains)
- Email-based (spoofed headers, malicious attachments)
- Visual-based (brand impersonation, fake login pages)

**Format**: Create ASCII art or detailed textual diagram showing:
```
                    PHISHING ATTACK LANDSCAPE
                           │
            ┌──────────────┼──────────────┐
            │              │              │
            ▼              ▼              ▼
      ┌──────────┐   ┌──────────┐   ┌──────────┐
      │   URL    │   │  Email   │   │  Visual  │
      │  Based   │   │  Based   │   │  Based   │
      └────┬─────┘   └────┬─────┘   └────┬─────┘
           │              │              │
    ┌──────┴──────┐ ┌─────┴──────┐ ┌─────┴──────┐
    │•Typosquatting│ │•Spoofing  │ │•Brand Fake │
    │•IDN Homograph│ │•Urgency   │ │•Logo Theft│
    │•Subdomain   │ │•Malicious │ │•Form Clone │
    │  Abuse      │ │  Links    │ │            │
    └─────────────┘ └────────────┘ └────────────┘
```

**Caption**: "Figure 1.1: The three primary vectors of phishing attacks addressed by this research."

**In-text Reference**: "As illustrated in Figure 1.1, modern phishing attacks have evolved to exploit multiple attack vectors, necessitating a multi-modal detection approach."

---

### Figure 1.2: Limitations of Existing Detection Methods
**Placement**: Section 1.2 (Problem Statement) - AFTER the primary problem description

**Description**: A comparison table/diagram showing:
- Signature-based: Fast but can't detect zero-day
- Deep Learning: Accurate but requires GPU
- Single-modal: Limited coverage
- API-based: Requires internet, privacy concerns

**Format**: Create a comparison matrix:
```
    Method          │ Zero-Day │ Resource │ Multi-Modal │ Privacy
    ────────────────┼──────────┼──────────┼─────────────┼─────────
    Signature-based │    ✗     │    ✓     │     ✗       │   ✓
    Deep Learning   │    ✓     │    ✗     │     ✓       │   ✓
    Single-Modal ML │    ✓     │    ✓     │     ✗       │   ✓
    API Services    │    ✓     │    ✓     │     ✓       │   ✗
    ────────────────┼──────────┼──────────┼─────────────┼─────────
    PHISHPULSE      │    ✓     │    ✓     │     ✓       │   ✓
```

**Caption**: "Figure 1.2: Comparison of existing phishing detection approaches against key requirements. Checkmarks (✓) indicate the method satisfies the requirement; crosses (✗) indicate limitations."

**In-text Reference**: "Figure 1.2 highlights the key limitations of current approaches, demonstrating the gap that PhishPulse aims to address through its hybrid unsupervised-supervised ensemble architecture."

---

## CHAPTER 2: LITERATURE REVIEW FIGURES

### Figure 2.1: Evolution of Phishing Detection Techniques Timeline
**Placement**: Section 2.2 (URL-Based Detection) - AT THE BEGINNING of the section

**Description**: A timeline showing the evolution from 2000 to 2024:
- 2000-2005: Blacklist/whitelist era
- 2005-2010: Heuristic rule-based systems
- 2010-2015: Machine learning classifiers (SVM, RF)
- 2015-2020: Deep learning approaches (CNN, LSTM)
- 2020-2024: Ensemble and multi-modal methods (including PhishPulse)

**Format**: Horizontal timeline with milestones:
```
2000      2005      2010      2015      2020      2024
 │         │         │         │         │         │
 ▼         ▼         ▼         ▼         ▼         ▼
[Blacklists]→[Heuristics]→[ML Classifiers]→[Deep Learning]→[Ensemble/Multi-Modal]
  └─────────┴─────────┴─────────┴─────────┴─────────┘
   │                    │                    │
   │                    │                    └─ PhishPulse (This Study)
   │                    └─ Isolation Forest
   └─ Yahoo! Anti-Spam
```

**Caption**: "Figure 2.1: Evolution of phishing detection methodologies from 2000 to 2024, showing the progression from simple blacklists to sophisticated ensemble approaches."

**In-text Reference**: "The evolution of phishing detection, depicted in Figure 2.1, demonstrates a clear trajectory toward increasingly sophisticated machine learning techniques."

---

### Figure 2.2: Isolation Forest Anomaly Detection Concept
**Placement**: Section 2.2.2 (Machine Learning Approaches) - WHEN discussing unsupervised methods

**Description**: Visual explanation of how Isolation Forest works:
- Show normal points requiring many splits to isolate
- Show anomalies isolated quickly with few splits
- Include a simple decision tree visualization

**Format**: ASCII representation:
```
Normal Data Point              Anomalous Data Point
       ●                              ●
       │                              │
   ┌───┴───┐                      ┌───┘
   │       │                      │
  ┌┴┐     ┌┴┐                   ┌┘
  │ │     │ │                   ●
  └┬┘     └┬┘
   │       │
  ┌┴┐     ┌┴┐
  │ │     │ │
  └┬┘     └┬┘
   │       │
  ●●●     ●●●

Path Length: 6 splits          Path Length: 2 splits
(High score = normal)          (Low score = anomaly)
```

**Caption**: "Figure 2.2: Conceptual illustration of Isolation Forest operation. Anomalies (right) are isolated with fewer random splits than normal points (left), resulting in shorter path lengths in the isolation trees."

**In-text Reference**: "As illustrated in Figure 2.2, Isolation Forest operates on the principle that anomalies are 'few and different,' requiring fewer splits to isolate in random decision trees (Liu et al., 2008)."

---

### Figure 2.3: Email Authentication Protocol Flow
**Placement**: Section 2.3.1 (Email Authentication Protocols) - AFTER introducing SPF, DKIM, DMARC

**Description**: Flow diagram showing how email authentication works:
1. Sender sends email
2. Receiving server checks SPF (IP authorized?)
3. Receiving server checks DKIM (signature valid?)
4. Receiving server checks DMARC (alignment?)
5. Decision: Accept, Quarantine, or Reject

**Format**: Flowchart:
```
┌──────────────┐     ┌─────────────────┐
│ Sender MTA   │────▶│ Recipient MTA   │
│ sends email  │     │ receives email  │
└──────────────┘     └────────┬────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ 1. SPF Check    │
                    │ Is sender IP    │
                    │ authorized?     │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
             PASS           FAIL          NEUTRAL
              │              │              │
              ▼              ▼              ▼
       ┌──────────┐   ┌──────────┐   ┌──────────┐
       │ Continue │   │ Continue │   │ Continue │
       │ to DKIM  │   │ to DKIM  │   │ to DKIM  │
       └──────────┘   └──────────┘   └──────────┘
                             │
                             ▼
                    [DKIM Check Block...]
                             │
                             ▼
                    [DMARC Check Block...]
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
            ACCEPT       QUARANTINE      REJECT
```

**Caption**: "Figure 2.3: Email authentication flow showing SPF, DKIM, and DMARC verification process in modern mail transfer agents."

**In-text Reference**: "The hierarchical verification process illustrated in Figure 2.3 forms the foundation of modern email authentication, though attackers frequently exploit misconfigurations or employ techniques that bypass these checks."

---

### Figure 2.4: Perceptual Hashing Concept
**Placement**: Section 2.4.2 (Computer Vision Approaches) - WHEN discussing pHash

**Description**: Show how perceptual hashing works:
- Original brand logo image → Resized → DCT → Hash
- Slightly modified image (different size, compression) → Same hash
- Completely different image → Different hash

**Format**: Visual comparison:
```
Original Image              Modified Image (resized)    Different Image
┌───────────┐               ┌───────┐                   ┌───────────┐
│ ╔═══════╗ │               │╔═════╗│                   │ ╔═══════╗ │
│ ║ PAYPAL║ │      →        │║PAY  ││                   │ ║ GOOGLE║ │
│ ╚═══════╝ │               │║PAL  ││                   │ ╚═══════╝ │
└───────────┘               └───────┘                   └───────────┘
      │                           │                           │
      ▼                           ▼                           ▼
┌───────────────┐           ┌───────────────┐           ┌───────────────┐
│ Resize to     │           │ Resize to     │           │ Resize to     │
│ 32x32         │           │ 32x32         │           │ 32x32         │
│ Grayscale     │           │ Grayscale     │           │ Grayscale     │
└───────┬───────┘           └───────┬───────┘           └───────┬───────┘
        │                           │                           │
        ▼                           ▼                           ▼
┌───────────────┐           ┌───────────────┐           ┌───────────────┐
│ DCT Transform │           │ DCT Transform │           │ DCT Transform │
└───────┬───────┘           └───────┬───────┘           └───────┬───────┘
        │                           │                           │
        ▼                           ▼                           ▼
┌───────────────┐           ┌───────────────┐           ┌───────────────┐
│ Hash:         │           │ Hash:         │           │ Hash:         │
│ a7f3c9d2...   │◄─────────▶│ a7f3c9d2...   │           │ b8e4d1a9...   │
│ (MATCH!)      │           │ (MATCH!)      │           │ (DIFFERENT)   │
└───────────────┘           └───────────────┘           └───────────────┘
```

**Caption**: "Figure 2.4: Conceptual illustration of perceptual hashing. Despite resizing, the modified PayPal logo generates the same hash as the original, while a different brand (Google) produces a distinct hash value."

**In-text Reference**: "Figure 2.4 demonstrates the robustness of perceptual hashing to benign transformations such as resizing and compression, making it ideal for detecting visual brand impersonation (Zauner, 2010)."

---

### Figure 2.5: Comparison of Existing Phishing Detection Systems
**Placement**: Section 2.7 (Existing Tools and Frameworks) - AT THE END of the section, BEFORE research gaps

**Description**: A comprehensive comparison table of existing systems vs. PhishPulse

**Format**: Large comparison table:
```
┌────────────────┬──────────┬───────────┬──────────┬──────────┬──────────┐
│ System         │ Approach │ Zero-Day  │ Resource │ Multi-   │ Open     │
│                │          │ Detection │ Efficient│ Modal    │ Source   │
├────────────────┼──────────┼───────────┼──────────┼──────────┼──────────┤
│ Google Safe    │Blacklist/│ Partial   │ Yes      │ No       │ No       │
│ Browsing       │Heuristic │           │          │          │          │
├────────────────┼──────────┼───────────┼──────────┼──────────┼──────────┤
│ VirusTotal     │Multi-AV  │ Yes       │ N/A      │ No       │ Partial  │
├────────────────┼──────────┼───────────┼──────────┼──────────┼──────────┤
│ PhishTank      │Community │ No        │ Yes      │ No       │ Yes      │
│                │Driven    │           │          │          │          │
├────────────────┼──────────┼───────────┼──────────┼──────────┼──────────┤
│ Phi-1 (2019)   │Deep URL  │ Yes       │ No       │ No       │ Yes      │
│                │Analysis  │           │ (GPU req)│          │          │
├────────────────┼──────────┼───────────┼──────────┼──────────┼──────────┤
│ EmailRep (2020)│ML + DNS  │ Partial   │ Yes      │ No       │ No       │
├────────────────┼──────────┼───────────┼──────────┼──────────┼──────────┤
│ LogoSENSE      │Visual    │ Yes       │ Yes      │ No       │ No       │
│ (2021)         │Only      │           │          │          │          │
├────────────────┼──────────┼───────────┼──────────┼──────────┼──────────┤
│ PHISHPULSE     │Ensemble  │ Yes       │ Yes      │ Yes      │ Yes      │
│ (This Study)   │Unsuper.  │           │          │          │          │
└────────────────┴──────────┴───────────┴──────────┴──────────┴──────────┘
```

**Caption**: "Figure 2.5: Comparison of existing phishing detection systems across key dimensions. PhishPulse uniquely combines zero-day detection, resource efficiency, multi-modal analysis, and open-source availability."

**In-text Reference**: "As summarized in Figure 2.5, existing solutions typically excel in only a subset of desirable characteristics, highlighting the need for an integrated approach such as that proposed in this study."

---

## CHAPTER 3: METHODOLOGY FIGURES

### Figure 3.1: Overall System Architecture
**Placement**: Section 3.2 (System Architecture Overview) - IMMEDIATELY AFTER the section heading

**Description**: The complete 4-model architecture showing data flow from input to output

**Format**: Detailed system diagram:
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          PHISHPULSE SYSTEM ARCHITECTURE                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INPUT LAYER                    PROCESSING LAYER              OUTPUT LAYER │
│                                                                             │
│  ┌───────────┐                                                               │
│  │   URL     │──┐                                                            │
│  └───────────┘  │                                                            │
│                 │         ┌───────────────┐                                  │
│  ┌───────────┐  │    ┌───▶│  Model A:     │──┐                               │
│  │   Email   │──┼───▶│    │  URL Lexical  │  │                               │
│  └───────────┘  │    │    │  Analyzer     │  │                               │
│                 │    │    │  (Isolation   │  │                               │
│  ┌───────────┐  │    │    │   Forest)     │  │                               │
│  │  Image/   │──┘    │    └───────────────┘  │                               │
│  │Screenshot │       │           │           │         ┌─────────────────┐    │
│  └───────────┘       │           │           │    ┌───▶│  Model D:       │    │
│                      │           │           │    │    │  Risk Fusion    │    │
│                      │    ┌──────┴──────┐    │    │    │  Engine         │───▶│
│                      │    │  Model B:   │────┼────┤    │  (Weighted      │    │
│                      └───▶│  Email      │    │    │    │   Ensemble)     │    │
│                           │  Forensic   │    │    │    └─────────────────┘    │
│                           │  Analyzer   │    │    │           │               │
│                           │  (Naive     │    │    │           │               │
│                           │   Bayes)    │    │    │           ▼               │
│                           └─────────────┘    │    │    ┌───────────────┐      │
│                                  │           │    └───▶│  Final Risk   │      │
│                           ┌──────┴──────┐    │         │  Score (0-100)│      │
│                           │  Model C:   │────┘         └───────┬───────┘      │
│                           │  Visual     │                      │              │
│                           │  Phishing   │                      ▼              │
│                           │  Detector   │              ┌───────────────┐      │
│                           │  (ORB +     │              │ Classification│      │
│                           │   pHash)    │              │ • Clean       │      │
│                           └─────────────┘              │ • Suspicious  │      │
│                                  │                     │ • Malicious   │      │
│                           ┌──────┴──────┐              │ • Critical    │      │
│                           │ Brand Logo  │              └───────────────┘      │
│                           │ Database    │                                     │
│                           └─────────────┘                                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Caption**: "Figure 3.1: Overall architecture of the PhishPulse system showing the four specialized models (A, B, C) feeding into the Risk Fusion Engine (D), which produces calibrated risk scores and classifications."

**In-text Reference**: "The proposed system architecture, depicted in Figure 3.1, employs a modular design with specialized analyzers for each attack vector, enabling both independent operation and ensemble-based decision making."

---

### Figure 3.2: URL Lexical Analyzer (Model A) Workflow
**Placement**: Section 3.4 (Model A) - AFTER the algorithm selection subsection

**Description**: Step-by-step flow of URL analysis from input to risk score

**Format**: Detailed workflow:
```
Input URL
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: URL Parsing                                         │
│  Parse: scheme, netloc, path, query, fragment               │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 2: Feature Extraction (16 features)                    │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ • Shannon Entropy    • Subdomain Depth                 ││
│  │ • URL Length         • Has IP Address                  ││
│  │ • Path Length        • Has @ Symbol                    ││
│  │ • Query Params       • Dash/Dot Count                  ││
│  │ • Suspicious TLD     • Digit Count                     ││
│  │ • Suspicious KWs     • Levenshtein Distance            ││
│  │ • HTTPS Flag         • Special Char Ratio              ││
│  └─────────────────────────────────────────────────────────┘│
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 3: Isolation Forest Prediction                         │
│  anomaly_score = model.decision_function(features)          │
│  risk_score = (0.5 - anomaly_score) × 100                   │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 4: Typosquatting Detection                             │
│  For each brand in TOP_BRANDS:                              │
│    distance = levenshtein(domain, brand)                    │
│    IF distance <= 2: flag as typosquatting                  │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
Output: {score: 85, indicators: [...], impersonated_brand: "paypal"}
```

**Caption**: "Figure 3.2: Detailed workflow of Model A (URL Lexical Analyzer) showing the four-stage processing pipeline from URL input to risk score output."

**In-text Reference**: "As detailed in Figure 3.2, the URL Lexical Analyzer follows a four-stage pipeline: parsing, feature extraction, anomaly detection, and typosquatting identification."

---

### Figure 3.3: Email Forensic Analysis Process
**Placement**: Section 3.5 (Model B) - AFTER feature extraction subsection

**Description**: Email analysis flow showing header parsing and content analysis

**Format**: Two-column analysis diagram:
```
┌────────────────────────────────────────────────────────────────────────────┐
│                     EMAIL FORENSIC ANALYSIS FLOW                           │
├─────────────────────────────────┬──────────────────────────────────────────┤
│  HEADER ANALYSIS                │  CONTENT ANALYSIS                        │
│                                 │                                          │
│  ┌─────────────────────────┐    │  ┌─────────────────────────────────┐    │
│  │ Parse Raw Email Headers │    │  │ Extract Body Text               │    │
│  └────────────┬────────────┘    │  └────────────┬────────────────────┘    │
│               │                 │               │                         │
│               ▼                 │               ▼                         │
│  ┌─────────────────────────┐    │  ┌─────────────────────────────────┐    │
│  │ Check Authentication:   │    │  │ TF-IDF Vectorization            │    │
│  │ • SPF (DNS TXT lookup)  │    │  │ HashingVectorizer(1024)         │    │
│  │ • DKIM (signature)      │    │  └────────────┬────────────────────┘    │
│  │ • DMARC (_dmarc record) │    │               │                         │
│  │ • Return-Path alignment │    │               ▼                         │
│  └────────────┬────────────┘    │  ┌─────────────────────────────────┐    │
│               │                 │  │ Naive Bayes Prediction          │    │
│               ▼                 │  │ P(phishing|features)            │    │
│  ┌─────────────────────────┐    │  └────────────┬────────────────────┘    │
│  │ Auth Score Calculation  │    │               │                         │
│  │ penalty = failures × 10 │    │               ▼                         │
│  └────────────┬────────────┘    │  ┌─────────────────────────────────┐    │
│               │                 │  │ Urgency Keyword Detection       │    │
│               │                 │  │ Count: "urgent", "verify", etc. │    │
│               │                 │  └────────────┬────────────────────┘    │
│               │                 │               │                         │
│               ▼                 │               ▼                         │
│  ┌─────────────────────────┐    │  ┌─────────────────────────────────┐    │
│  │    FINAL COMBINED       │◄───┼──│         SCORE                   │    │
│  │    RISK SCORE           │    │  │ score = nb_score + auth_penalty │    │
│  │                         │    │  │         + urgency_penalty       │    │
│  └─────────────────────────┘    │  └─────────────────────────────────┘    │
└─────────────────────────────────┴──────────────────────────────────────────┘
```

**Caption**: "Figure 3.3: Parallel processing flow of Model B (Email Forensic Analyzer) showing the dual-track analysis of authentication headers (left) and semantic content (right), which are fused into a final risk score."

**In-text Reference**: "Figure 3.3 illustrates the parallel processing architecture of the Email Forensic Analyzer, which independently evaluates authentication protocols and semantic content before combining evidence (Metsis et al., 2006)."

---

### Figure 3.4: Visual Phishing Detection Pipeline
**Placement**: Section 3.6 (Model C) - AFTER algorithm selection subsection

**Description**: Visual detection showing ORB and pHash processing in parallel

**Format**: Visual processing diagram:
```
Input Image (Screenshot/Logo)
            │
            ▼
┌─────────────────────────────────────────────────────────────┐
│  PREPROCESSING                                               │
│  • Convert to OpenCV format                                 │
│  • Resize to standard dimensions                            │
│  • Convert to RGB if necessary                              │
└────────────────┬────────────────────────────────────────────┘
                 │
     ┌───────────┴───────────┐
     │                       │
     ▼                       ▼
┌──────────────────┐  ┌──────────────────┐
│  pHash Branch    │  │  ORB Branch      │
│                  │  │                  │
│  ┌────────────┐  │  │  ┌────────────┐  │
│  │ DCT        │  │  │  │ Convert to │  │
│  │ Transform  │  │  │  │ Grayscale  │  │
│  └─────┬──────┘  │  │  └─────┬──────┘  │
│        │         │  │        │         │
│        ▼         │  │        ▼         │
│  ┌────────────┐  │  │  ┌────────────┐  │
│  │ Generate   │  │  │  │ Detect     │  │
│  │ 64-bit Hash│  │  │  │ 500 ORB    │  │
│  └─────┬──────┘  │  │  │ Features   │  │
│        │         │  │  └─────┬──────┘  │
│        ▼         │  │        │         │
│  ┌────────────┐  │  │        ▼         │
│  │ Compare to │  │  │  ┌────────────┐  │
│  │ Brand DB   │  │  │  │ BFMatcher  │  │
│  │ (Hamming)  │  │  │  │ Comparison │  │
│  └─────┬──────┘  │  │  └─────┬──────┘  │
│        │         │  │        │         │
│        ▼         │  │        ▼         │
│  ┌────────────┐  │  │  ┌────────────┐  │
│  │ Confidence │  │  │  │ Match      │  │
│  │ = 1 - d/64 │  │  │  │ Count      │  │
│  └─────┬──────┘  │  │  └─────┬──────┘  │
└────────┼────────┘  └────────┼────────┘
         │                    │
         └──────────┬─────────┘
                    │
                    ▼
         ┌──────────────────┐
         │  SCORE FUSION    │
         │  Combine pHash   │
         │  and ORB scores  │
         └────────┬─────────┘
                  │
                  ▼
         ┌──────────────────┐
         │  FORM DETECTION  │
         │  (Bonus check)   │
         │  Credential      │
         │  fields present? │
         └────────┬─────────┘
                  │
                  ▼
         Output: {score, brand_match, confidence}
```

**Caption**: "Figure 3.4: Visual Phishing Detector pipeline showing parallel pHash and ORB processing branches, with subsequent score fusion and form field detection for credential harvesting identification."

**In-text Reference**: "The dual-branch architecture depicted in Figure 3.4 leverages both global image similarity (via pHash) and local feature matching (via ORB) to achieve robust brand impersonation detection without requiring training on phishing images (Rublee et al., 2011)."

---

### Figure 3.5: Risk Fusion Engine Decision Process
**Placement**: Section 3.7 (Model D) - AT THE BEGINNING of the section

**Description**: How the weighted ensemble combines scores and makes final decisions

**Format**: Decision tree/flow diagram:
```
┌──────────────────────────────────────────────────────────────────────────┐
│                    RISK FUSION ENGINE (MODEL D)                          │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Input Scores from Models A, B, C                                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                               │
│  │ URL: 85  │  │ Email: 0 │  │ Visual:90│                               │
│  │ (weight  │  │ (weight  │  │ (weight  │                               │
│  │  0.30)   │  │  0.35)   │  │  0.35)   │                               │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘                               │
│       │             │             │                                      │
│       └─────────────┼─────────────┘                                      │
│                     │                                                    │
│                     ▼                                                    │
│       ┌─────────────────────────┐                                       │
│       │ WEIGHTED SUM CALCULATION│                                       │
│       │                         │                                       │
│       │ score = (85 × 0.30) +   │                                       │
│       │         (0 × 0.35) +    │                                       │
│       │         (90 × 0.35)     │                                       │
│       │       = 25.5 + 0 + 31.5 │                                       │
│       │       = 57.0            │                                       │
│       └───────────┬─────────────┘                                       │
│                   │                                                      │
│                   ▼                                                      │
│       ┌─────────────────────────┐                                       │
│       │ DYNAMIC ADJUSTMENTS     │                                       │
│       │                         │                                       │
│       │ Domain age < 7 days?    │                                       │
│       │   YES → +20 points      │                                       │
│       │                         │                                       │
│       │ Invalid SSL?            │                                       │
│       │   NO → +0 points        │                                       │
│       │                         │                                       │
│       │ Adjusted Score = 77     │                                       │
│       └───────────┬─────────────┘                                       │
│                   │                                                      │
│                   ▼                                                      │
│       ┌─────────────────────────┐                                       │
│       │ CONFIDENCE CALIBRATION  │                                       │
│       │                         │                                       │
│       │ Isotonic Regression or  │                                       │
│       │ Sigmoid Calibration       │                                       │
│       │                         │                                       │
│       │ 95% CI Calculation:     │                                       │
│       │ [0.72, 0.92]            │                                       │
│       └───────────┬─────────────┘                                       │
│                   │                                                      │
│                   ▼                                                      │
│       ┌─────────────────────────┐                                       │
│       │ CLASSIFICATION          │                                       │
│       │                         │      ┌──────────────┐                 │
│       │ Score = 77              │─────▶│  MALICIOUS   │                 │
│       │ 61-85 range             │      │   (RED)      │                 │
│       │                         │      └──────────────┘                 │
│       └─────────────────────────┘                                       │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

**Caption**: "Figure 3.5: Risk Fusion Engine decision process showing weighted score calculation, dynamic adjustments for domain age and SSL validity, confidence calibration, and final classification into risk categories."

**In-text Reference**: "The multi-stage fusion process illustrated in Figure 3.5 enables dynamic risk assessment by combining model predictions with external threat intelligence (domain age, SSL status) and calibrating confidence for security-critical decision making."

---

### Figure 3.6: Database Entity-Relationship Diagram
**Placement**: Section 3.8.2 (Database Schema) - IMMEDIATELY AFTER subsection heading

**Description**: ER diagram showing all tables and relationships

**Format**: ER diagram:
```
┌──────────────────────┐         ┌──────────────────────┐
│      SCAN            │         │      REPORT          │
├──────────────────────┤         ├──────────────────────┤
│ PK id: UUID          │◄────────│ FK scan_id           │
│    timestamp         │   1:1   │    file_path         │
│    scan_type         │         │    file_size         │
│    target            │         │    created_at        │
│    final_score       │         └──────────────────────┘
│    classification    │
│    confidence_lower  │
│    confidence_upper  │
│    url_score         │
│    email_score       │
│    visual_score      │
│    indicators[]      │
│    mitigation_steps[]│
│    domain_age_days   │
│    has_valid_ssl     │
│    impersonated_brand│
│    report_generated  │
└──────────┬───────────┘
           │
           │ 1:N (optional - cache feature history)
           │
    ┌──────┴──────┐
    │             │
    ▼             ▼
┌──────────────────────┐    ┌──────────────────────┐    ┌──────────────────────┐
│   URLFEATURE         │    │   EMAILFEATURE       │    │   VISUALHASH         │
├──────────────────────┤    ├──────────────────────┤    ├──────────────────────┤
│ PK id: UUID          │    │ PK id: UUID          │    │ PK id: UUID          │
│    url: UNIQUE       │    │    email_hash: UNIQUE│    │    brand_name        │
│    entropy           │    │    spf_aligned       │    │    phash             │
│    levenshtein_dist  │    │    dkim_aligned      │    │    image_path        │
│    subdomain_depth   │    │    dmarc_aligned     │    │    created_at        │
│    tld_risk          │    │    return_path_match │    └──────────────────────┘
│    has_suspicious_kw │    │    urgency_score     │
│    created_at        │    │    html_text_ratio   │
└──────────────────────┘    │    created_at        │
                            └──────────────────────┘
```

**Caption**: "Figure 3.6: Entity-Relationship diagram of the PhishPulse database schema. The central Scan table maintains relationships with Report (one-to-one) and feature cache tables (one-to-many), while VisualHash maintains the brand logo perceptual hash database."

**In-text Reference**: "The database schema, depicted in Figure 3.6, employs a normalized relational design with the Scan entity at the center, maintaining referential integrity with generated reports and cached feature extractions for performance optimization."

---

## SUMMARY OF FIGURES BY CHAPTER

| Chapter | Figure | Title | Section | Approx. Position |
|---------|--------|-------|---------|------------------|
| 1 | 1.1 | Phishing Attack Landscape | 1.1 | After para 2 |
| 1 | 1.2 | Limitations of Existing Methods | 1.2 | After problem statement |
| 2 | 2.1 | Evolution Timeline | 2.2 | Beginning of section |
| 2 | 2.2 | Isolation Forest Concept | 2.2.2 | With unsupervised methods |
| 2 | 2.3 | Email Authentication Flow | 2.3.1 | After protocol introduction |
| 2 | 2.4 | Perceptual Hashing | 2.4.2 | When discussing pHash |
| 2 | 2.5 | System Comparison Table | 2.7 | End of section |
| 3 | 3.1 | System Architecture | 3.2 | Immediately after heading |
| 3 | 3.2 | URL Analyzer Workflow | 3.4 | After algorithm selection |
| 3 | 3.3 | Email Analysis Process | 3.5 | After feature extraction |
| 3 | 3.4 | Visual Detection Pipeline | 3.6 | After algorithm selection |
| 3 | 3.5 | Risk Fusion Process | 3.7 | Beginning of section |
| 3 | 3.6 | Database ER Diagram | 3.8.2 | Immediately after heading |

---

## FORMAT SPECIFICATIONS

### For ASCII Art Figures:
- Use monospace font
- Include borders/boxes where appropriate
- Use arrows (→, ▶, ▼) to show flow
- Keep line length under 80 characters for PDF compatibility
- Use consistent spacing

### For Tables:
- Use box-drawing characters (┌─┬─┐) for professional appearance
- Include column headers
- Align data consistently
- Add units where applicable

### Captions Format:
```
Figure X.Y: [Descriptive title in sentence case]. [Optional additional explanation.]
```

### In-text Reference Format:
```
As illustrated in Figure X.Y, ...
The process depicted in Figure X.Y demonstrates...
Figure X.Y illustrates the...
```

---

## INSTRUCTIONS FOR KIMI

1. **Create figures AS YOU WRITE** each section - don't wait until the end
2. **Insert figure immediately** after the in-text reference sentence
3. **Use consistent figure numbering** - Chapter.Figure format (1.1, 1.2, 2.1, etc.)
4. **Make figures self-contained** - Reader should understand without reading all text
5. **Keep ASCII art clean** - Use spaces consistently, align characters
6. **Reference each figure in text** - Every figure must be mentioned before it appears
7. **Caption below figure** - Standard academic practice
8. **Complex diagrams** - If ASCII is insufficient, provide detailed description for external creation

---

## ADDITIONAL NOTES

### For Complex Visualizations (Chapters 4-5):
These will need actual generated images (not ASCII):
- ROC curves (Matplotlib)
- Confusion matrices (Seaborn heatmap)
- Performance bar charts
- System screenshots

**Recommendation**: For these, write placeholder text like:
```
[FIGURE 5.1: ROC curve comparing Model A, B, C, and ensemble performance. 
TO BE GENERATED: Use Python matplotlib to plot True Positive Rate vs 
False Positive Rate for each model.]
```

### Color Coding (if supported):
If the output format supports color, use these conventions:
- 🔴 Red: Critical/Malicious
- 🟡 Yellow: Suspicious  
- 🟢 Green: Clean/Safe
- 🔵 Blue: Process/Flow
- ⚫ Black/White: Neutral/Data

### Alternative for Chapter 3:
If ASCII art is too limiting for complex architecture diagrams, provide:
1. **Mermaid diagram code** (can be rendered by many tools)
2. **Graphviz DOT code** (for automatic generation)
3. **Detailed description** for manual drawing in PowerPoint/Draw.io

---

**TOTAL FIGURES TO CREATE: 13 figures across Chapters 1-3**
