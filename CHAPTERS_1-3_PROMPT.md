# Prompt for Kimi: Write PhishPulse Thesis Chapters 1-3

## Document Information
- **Project**: PhishPulse v2.0 - Real-Time Multi-Modal Phishing Detection Engine
- **Document Type**: B.Sc./M.Sc. Thesis or Academic Dissertation
- **Course Context**: CSC 405 - Artificial Intelligence in Cybersecurity
- **Chapters to Write**: Chapter 1 (Introduction), Chapter 2 (Literature Review), Chapter 3 (Methodology)
- **Target Length**: 15,000-25,000 words total
- **Citation Style**: APA 7th Edition or IEEE

---

## PROJECT CONTEXT SUMMARY

**PhishPulse** is a production-grade, four-model ensemble cybersecurity framework for real-time phishing detection across URL, email, and visual attack vectors. Key innovations:

- **Hybrid AI Architecture**: Combines unsupervised anomaly detection (Isolation Forests, perceptual hashing) with supervised forensic analysis (Naive Bayes, heuristics)
- **Resource-Optimized**: Runs on 7.4GB RAM, CPU-only inference
- **Multi-Modal**: Analyzes URLs, emails, and visual content simultaneously
- **Zero-Day Detection**: Isolation Forests trained exclusively on benign data detect novel threats
- **4-Model Ensemble**:
  - Model A: URL Lexical Analyzer (Isolation Forest + Regex)
  - Model B: Email Forensic Analyzer (Naive Bayes + Header Analysis)
  - Model C: Visual Phishing Detector (ORB + pHash)
  - Model D: Risk Fusion Engine (Weighted Ensemble + Isotonic Regression)

**Technical Stack**: Python, FastAPI, scikit-learn, OpenCV, SQLite, React, Playwright

---

## CHAPTER 1: INTRODUCTION (4,000-6,000 words)

### 1.1 Background of the Study
- Define phishing and its evolution as a cyber threat
- Statistics on global phishing attacks and economic impact
- Current phishing techniques (URL-based, email-based, visual impersonation)
- Limitations of existing detection methods
- The role of AI/ML in cybersecurity

### 1.2 Problem Statement
- **Primary Problem**: Existing phishing detection systems rely on signature-based methods that cannot detect zero-day attacks
- **Secondary Problems**:
  - High computational requirements of deep learning solutions
  - Lack of multi-modal analysis (URL + Email + Visual)
  - Poor calibration of confidence scores in security contexts
  - Need for labeled malicious datasets for supervised learning
- **Gap in Knowledge**: Need for hybrid unsupervised-supervised approaches optimized for resource-constrained environments

### 1.3 Research Questions
1. How effective is unsupervised anomaly detection using Isolation Forests trained exclusively on benign data for identifying novel phishing URLs?
2. Can a weighted ensemble of specialized models (URL, Email, Visual) achieve higher accuracy than monolithic approaches?
3. How can multi-modal risk fusion be calibrated for security-critical applications?
4. What is the optimal balance between detection accuracy and computational efficiency for real-time phishing detection?

### 1.4 Research Objectives

**Main Objective**:
To develop and evaluate a resource-efficient, multi-modal phishing detection system using hybrid unsupervised-supervised machine learning techniques.

**Specific Objectives**:
1. To implement an Isolation Forest-based URL analyzer trained solely on benign CommonCrawl data
2. To develop an email forensic analyzer combining Naive Bayes classification with authentication protocol validation
3. To create a visual phishing detector using ORB features and perceptual hashing without requiring labeled phishing images
4. To design a risk fusion engine that aggregates multi-modal signals with calibrated confidence intervals
5. To evaluate system performance against benchmark datasets and compare with existing solutions

### 1.5 Scope and Delimitations

**Scope**:
- URL-based phishing detection via lexical analysis
- Email phishing detection via content and header analysis
- Visual brand impersonation detection
- Real-time inference with sub-second latency
- Browser extension and web dashboard interfaces

**Delimitations**:
- Focus on English-language phishing content
- Does not include malware detection
- Does not analyze JavaScript behavior (static analysis only)
- Limited to known brand database for visual detection
- CPU-only deployment (no GPU acceleration)

### 1.6 Significance of the Study

**Theoretical Significance**:
- Contributes to knowledge on unsupervised anomaly detection for cybersecurity
- Demonstrates effectiveness of multi-modal ensemble methods in phishing detection
- Provides calibration methodology for security-critical ML applications

**Practical Significance**:
- Provides deployable tool for organizations with limited computational resources
- Reduces dependency on constantly updated threat signatures
- Offers explainable AI approach with indicator-based reporting

### 1.7 Definition of Terms
- **Phishing**: Fraudulent attempt to obtain sensitive information...
- **Typosquatting**: URL-based attack using visually similar domain names...
- **Isolation Forest**: Unsupervised anomaly detection algorithm...
- **Perceptual Hashing**: Image fingerprinting technique robust to minor modifications...
- **ORB (Oriented FAST and Rotated BRIEF)**: Computer vision feature detection algorithm...
- **Risk Fusion**: Multi-model signal aggregation methodology...

### 1.8 Thesis Organization
Brief overview of each chapter:
- Chapter 2: Literature review of phishing detection techniques
- Chapter 3: Methodology and system design
- Chapter 4: Implementation details
- Chapter 5: Results and evaluation
- Chapter 6: Conclusion and future work

---

## CHAPTER 2: LITERATURE REVIEW (6,000-10,000 words)

### 2.1 Introduction to Phishing Attacks
2.1.1 History and Evolution of Phishing
2.1.2 Types of Phishing Attacks
  - Deceptive phishing
  - Spear phishing
  - Whaling
  - Clone phishing
  - HTTPS phishing
  - Visual/graphical phishing
2.1.3 Phishing Attack Chain (MITRE ATT&CK Framework)

### 2.2 URL-Based Phishing Detection
2.2.1 Heuristic and Rule-Based Methods
  - Blacklist/whitelist approaches
  - Regular expression patterns
  - Limitations and evasion techniques

2.2.2 Machine Learning Approaches for URLs
  - Feature extraction methods (lexical, host-based, content-based)
  - Supervised learning (SVM, Random Forest, Neural Networks)
  - **Unsupervised learning approaches** (focus on Isolation Forest, One-Class SVM)
  - Deep learning approaches (CNN, LSTM for URL sequences)

2.2.3 Limitations of Existing URL Detection Methods
  - Requirement for labeled malicious samples
  - Concept drift in phishing tactics
  - Short-lived phishing URLs
  - Polymorphic attacks

### 2.3 Email Phishing Detection
2.3.1 Email Authentication Protocols
  - SPF (Sender Policy Framework)
  - DKIM (DomainKeys Identified Mail)
  - DMARC (Domain-based Message Authentication)
  - BIMI (Brand Indicators for Message Identification)

2.3.2 Content-Based Email Analysis
  - Header analysis techniques
  - Natural Language Processing for phishing detection
  - TF-IDF and Bag-of-Words approaches
  - Sentiment and urgency detection

2.3.3 Behavioral Analysis
  - Sender reputation systems
  - Graph-based email network analysis
  - User behavior modeling

### 2.4 Visual Phishing Detection
2.4.1 Brand Impersonation Attacks
  - Visual similarity attacks
  - Logo and trademark abuse
  - Website cloning techniques

2.4.2 Computer Vision Approaches
  - Template matching methods
  - Feature-based detection (SIFT, SURF, ORB)
  - Deep learning approaches (CNN, Siamese networks)
  - Perceptual hashing techniques (pHash, dHash, aHash)

2.4.3 Visual-Textual Consistency
  - Multi-modal analysis combining visual and textual cues
  - Layout analysis for credential forms

### 2.5 Ensemble and Multi-Modal Methods
2.5.1 Ensemble Learning in Cybersecurity
  - Voting-based ensembles
  - Stacking and boosting methods
  - Weighted combination strategies

2.5.2 Multi-Modal Phishing Detection
  - Fusion of URL, content, and visual features
  - Decision-level vs. feature-level fusion
  - Confidence calibration techniques
  - Isotonic regression for probability calibration

### 2.6 Resource-Constrained Machine Learning
2.6.1 Edge Computing for Security
  - Model compression techniques
  - Knowledge distillation
  - Quantization and pruning

2.6.2 Lightweight ML Algorithms
  - Isolation Forest computational efficiency
  - Naive Bayes for text classification
  - Traditional CV vs. deep learning for embedded systems

### 2.7 Existing Tools and Frameworks
2.7.1 Commercial Solutions
  - Google Safe Browsing
  - Microsoft Defender SmartScreen
  - PhishTank
  - VirusTotal

2.7.2 Academic and Open Source Systems
  - Phi-1 (URL-only)
  - Email phishing detectors
  - Visual similarity tools
  - Limitations of current integrated solutions

### 2.8 Research Gaps and Opportunities
- Gap 1: Lack of unified multi-modal frameworks
- Gap 2: Dependency on GPU resources for visual detection
- Gap 3: Need for zero-day detection without malicious training data
- Gap 4: Poor confidence calibration in security ML systems
- **How this study addresses these gaps**

### 2.9 Theoretical Framework
- Anomaly Detection Theory
- Ensemble Learning Theory
- Signal Detection Theory (ROC analysis, precision-recall trade-offs)
- Multi-Modal Fusion Theory

### 2.10 Summary
Synthesis of literature leading to the proposed solution...

---

## CHAPTER 3: METHODOLOGY (5,000-9,000 words)

### 3.1 Research Design
- **Type**: Design Science Research (DSR) / Engineering Research
- **Approach**: Quantitative evaluation with benchmark datasets
- **Validation Strategy**: Time-based train-test splits, cross-validation
- **Evaluation Metrics**: Accuracy, Precision, Recall, F1-Score, AUC-ROC, Inference Time

### 3.2 System Architecture Overview

**High-Level Architecture Diagram** (describe in text):
```
Input Layer → Analysis Layer → Fusion Layer → Output Layer
   │              │               │              │
   │         ┌────┴────┐          │         ┌────┴────┐
   │         │ Model A │          │         │ Risk    │
   │         │ (URL)   │          │         │ Score   │
   │         └────┬────┘          │         └────┬────┘
   │              │               │              │
Input URL   ┌────┴────┐     ┌─────┴─────┐   Classification
or Email    │ Model B │     │  Model D  │   PDF Report
or Image →  │ (Email) │────▶│(Ensemble) │────────▶
            └────┬────┘     └─────┬─────┘
                 │                │
            ┌────┴────┐           │
            │ Model C │           │
            │(Visual) │           │
            └─────────┘           │
         Brand Logo DB            │
```

### 3.3 Data Collection and Datasets

3.3.1 **URL Dataset**
- Source: Majestic Million (top 1 million websites)
- Size: 100,000 benign URLs for training
- Format: CSV (GlobalRank, TldRank, Domain, TLD)
- Preprocessing: URL normalization, feature extraction

3.3.2 **Email Dataset**
- Source: Enron Email Dataset (benign) + Enron Spam Dataset
- Size: ~500,000 emails total
- Distribution: 95% benign, 5% spam
- Features: Subject, body, headers (From, Return-Path, Authentication-Results)

3.3.3 **Visual Dataset**
- Source: Logo-2K+ dataset, brand websites
- Brands: 20 major brands (PayPal, Microsoft, Google, Apple, Amazon, etc.)
- Variations: Multiple logos per brand (different resolutions, formats)
- Processing: Perceptual hash generation, ORB descriptor extraction

3.3.4 **Test Datasets**
- PhishTank (real phishing URLs)
- URLHaus (malicious URL feed)
- Custom collected phishing emails
- Synthesized visual phishing screenshots

### 3.4 Model A: URL Lexical Analyzer

3.4.1 **Algorithm Selection: Isolation Forest**
- Why Isolation Forest for unsupervised anomaly detection
- Mathematical foundation: path length in random trees
- Advantages: Linear time complexity, handles high dimensions, no malicious training data needed

3.4.2 **Feature Engineering**
List and explain all 16 features:
1. Shannon Entropy (DGA detection)
2. URL Length (normalized)
3. Path Length (normalized)
4. Query Parameter Count
5. Subdomain Depth
6. Has IP Address (binary)
7. Has @ Symbol (binary)
8. Has Double Slash (binary)
9. Dash Count (normalized)
10. Dot Count (normalized)
11. Digit Count (normalized)
12. Suspicious Keyword Count
13. TLD Risk Score
14. Levenshtein Distance (min to top brands)
15. Has HTTPS (binary)
16. Special Character Ratio

3.4.3 **Typosquatting Detection**
- Levenshtein distance calculation
- Brand database (top 20 brands)
- Attack classification: substitution, omission, addition, swap

3.4.4 **Training Process**
- Training on benign data only
- Contamination parameter: 0.1 (expected anomaly ratio)
- n_estimators: 100 trees
- Model compression with joblib (level 3)

### 3.5 Model B: Email Forensic Analyzer

3.5.1 **Algorithm Selection: Multinomial Naive Bayes**
- Why Naive Bayes for text classification
- Independence assumption and its validity for email features
- Memory efficiency for large-scale deployment

3.5.2 **TF-IDF Vectorization**
- HashingVectorizer with 1024 features (memory optimization)
- n-gram range: (1, 2) for word combinations
- Why not traditional TF-IDF: stateless, constant memory

3.5.3 **Feature Extraction**
- SPF/DKIM/DMARC validation via DNS queries
- Return-Path vs From header comparison
- Urgency keyword detection (15 predefined keywords)
- HTML-to-text ratio for obfuscation detection
- Link analysis (visible text vs href mismatch)

3.5.4 **Incremental Training**
- partial_fit() for batch processing
- Batch size: 500 emails
- Classes: [0, 1] (benign, phishing)

### 3.6 Model C: Visual Phishing Detector

3.6.1 **Algorithm Selection: ORB + Perceptual Hashing**
- Why ORB over SIFT/SURF (patent-free, faster)
- Perceptual hashing for robust similarity matching
- Unsupervised approach: no phishing images needed

3.6.2 **Perceptual Hashing (pHash)**
- Discrete Cosine Transform (DCT) of resized image
- 64-bit hash generation
- Hamming distance comparison (threshold: 10)
- Database storage in SQLite

3.6.3 **ORB Feature Extraction**
- 500 ORB features per image
- Brute-Force Hamming matcher
- Cross-check for robust matching
- Good match threshold: distance < 50

3.6.4 **Form Field Detection**
- Edge detection with Canny algorithm
- Contour detection for rectangular regions
- Aspect ratio filtering (2-10 width/height)
- Size thresholds for input fields

3.6.5 **Brand Database Construction**
- Logo collection from official sources
- Multiple variants per brand
- Hash pre-computation for fast lookup

### 3.7 Model D: Risk Fusion Engine

3.7.1 **Weighted Voting Ensemble**
- Weight assignment rationale:
  - URL: 30% (structural but can be obfuscated)
  - Email: 35% (high confidence with auth protocols)
  - Visual: 35% (strong signal but not always present)
- Dynamic weight adjustment based on availability

3.7.2 **Dynamic Risk Adjustments**
- Domain age penalty: +20 if < 7 days
- SSL invalid penalty: +15 points
- Rationale for penalty values

3.7.3 **Confidence Calibration**
- Isotonic Regression for probability calibration
- 95% Confidence Interval calculation using model variance
- Formula: CI = base_prob ± 1.96 × (std_dev / 100)

3.7.4 **Classification Thresholds**
- Clean (0-30): No action required
- Suspicious (31-60): Review recommended
- Malicious (61-85): Block immediately
- Critical (86-100): Incident response

### 3.8 System Implementation

3.8.1 **Backend Architecture**
- FastAPI framework (async Python)
- SQLAlchemy ORM with SQLite
- Pydantic models for validation
- Middleware: CORS, request timing, error handling

3.8.2 **Database Schema**
- Scan table: store all scan results
- Report table: PDF forensic reports
- Feature cache tables for performance
- Visual hash table for brand matching

3.8.3 **API Design**
- RESTful endpoints
- POST /api/v1/scan - Unified scan endpoint
- GET /api/v1/scan/{id} - Retrieve scan results
- Authentication: JWT tokens (optional)

3.8.4 **Frontend Implementation**
- React 18 with Vite
- Tailwind CSS for styling
- Axios for API communication
- React Router for navigation

3.8.5 **Browser Extension**
- Manifest V3 for Chrome/Firefox/Edge
- Content scripts for Gmail/Outlook integration
- Background service worker
- Popup interface for manual scans

### 3.9 Evaluation Methodology

3.9.1 **Performance Metrics**
- True Positives (TP), False Positives (FP)
- True Negatives (TN), False Negatives (FN)
- Accuracy = (TP + TN) / Total
- Precision = TP / (TP + FP)
- Recall = TP / (TP + FN)
- F1-Score = 2 × (Precision × Recall) / (Precision + Recall)
- AUC-ROC for threshold-independent evaluation

3.9.2 **Benchmark Comparisons**
- Google Safe Browsing API
- PhishTank detection rates
- Academic baseline systems
- Single-model vs. ensemble comparison

3.9.3 **Ablation Studies**
- Effect of removing each model from ensemble
- Feature importance analysis
- Weight sensitivity analysis

3.9.4 **Computational Performance**
- Inference time measurement (ms)
- Memory usage profiling
- Throughput (requests/second)
- Scalability testing

### 3.10 Ethical Considerations
- Use of public datasets (Enron, CommonCrawl)
- No real user data in training
- Responsible disclosure of detected phishing
- Privacy-preserving design (local processing)

### 3.11 Summary
Recap of methodology approach and expected outcomes...

---

## WRITING GUIDELINES

### Tone and Style
- **Academic and formal** - Avoid casual language
- **Technical precision** - Use correct ML/cybersecurity terminology
- **Active voice** where appropriate ("This study proposes...", "We implement...")
- **Third person** for objectivity

### Formatting Requirements
- Font: Times New Roman, 12pt
- Line spacing: 1.5 or double-spaced
- Margins: 1 inch (2.54 cm) all sides
- Page numbers: Bottom center
- Chapter headings: 16pt bold
- Section headings: 14pt bold
- Subsection headings: 12pt bold

### Citation Requirements
- Minimum 50 references for Chapters 1-2
- Mix of:
  - Seminal works (classic papers in the field)
  - Recent publications (2019-2024) - at least 30%
  - Conference papers (IEEE, ACM, major security conferences)
  - Journal articles (high-impact: TDSC, TIFS, Computers & Security)

### Figure and Table Guidelines
- **Minimum 5 figures** in Chapter 3 (architecture, flowcharts, diagrams)
- **Minimum 5 tables** (comparison of methods, datasets, features)
- All figures must have captions below (Figure X.Y: Description)
- All tables must have captions above (Table X.Y: Description)
- Use placeholder markers like [FIGURE 3.1: System Architecture Diagram]

### Equations
- Use LaTeX formatting for mathematical expressions
- Number important equations: (3.1), (3.2), etc.
- Key equations to include:
  - Isolation Forest anomaly score calculation
  - Naive Bayes probability formula
  - Weighted ensemble calculation
  - Confidence interval formula
  - Hamming distance for perceptual hashing

### Code Snippets
- Include brief pseudocode or Python snippets for key algorithms
- Use monospace font for code
- Maximum 10 lines per snippet (reference full code in appendix)

---

## KEY REFERENCES TO INCLUDE

### Essential Citations (Must Include)

**Phishing Detection Foundations:**
1. APWG Phishing Activity Trends Reports (latest)
2. Verizon DBIR (Data Breach Investigations Report) - latest
3. Microsoft Digital Defense Report - latest

**Isolation Forest:**
4. Liu, F. T., Ting, K. M., & Zhou, Z. H. (2008). Isolation forest. ICDM 2008.

**Naive Bayes for Email:**
5. Metsis, V., Androutsopoulos, I., & Paliouras, G. (2006). Spam filtering with Naive Bayes.

**Perceptual Hashing:**
6. Zauner, C. (2010). Implementation and benchmarking of perceptual image hash functions.

**ORB Features:**
7. Rublee, E., et al. (2011). ORB: An efficient alternative to SIFT or SURF. ICCV 2011.

**Ensemble Methods:**
8. Zhou, Z. H. (2012). Ensemble Methods: Foundations and Algorithms.

**Confidence Calibration:**
9. Zadrozny, B., & Elkan, C. (2002). Transforming classifier scores into accurate multiclass probability estimates.

**FastAPI/Modern Web:**
10. Ramalho, L. (2022). Fluent Python (2nd ed.) - for implementation context

### Additional Suggested Topics to Research
- Deep learning phishing detection (for comparison)
- Browser security extensions
- SPF/DKIM/DMARC protocols (RFC specifications)
- MITRE ATT&CK phishing techniques
- Graph neural networks for phishing (recent trend)
- Federated learning for security (emerging area)

---

## CHAPTER-SPECIFIC DELIVERABLES

### Chapter 1 Deliverables
- [ ] Compelling hook/attention grabber in first paragraph
- [ ] Clear problem statement with bullet points
- [ ] 4 well-formed research questions
- [ ] 5 specific, measurable objectives
- [ ] Clear scope boundaries (inclusions and exclusions)
- [ ] Significance with both theoretical and practical components
- [ ] Comprehensive definition of 8-10 key terms

### Chapter 2 Deliverables
- [ ] At least 50 citations
- [ ] Coverage of all 3 attack vectors (URL, Email, Visual)
- [ ] Table comparing existing tools/frameworks (at least 8 systems)
- [ ] Clear identification of 4 research gaps
- [ ] Synthesis leading to proposed solution
- [ ] Theoretical framework section connecting theories to approach

### Chapter 3 Deliverables
- [ ] Complete system architecture description
- [ ] Detailed feature lists for all models
- [ ] Algorithm selection justification for each model
- [ ] Mathematical formulations of key algorithms
- [ ] Dataset descriptions with sizes and sources
- [ ] Evaluation metrics formulas
- [ ] Ethical considerations section
- [ ] Figure placeholders for diagrams (minimum 5)

---

## QUALITY CHECKLIST

Before finalizing each chapter, verify:

- [ ] **Coherence**: Each paragraph flows logically to the next
- [ ] **Citation Balance**: Every major claim has a citation
- [ ] **Recency**: At least 30% of references are from 2019-2024
- [ ] **Originality**: Plagiarism check passed (< 15% similarity)
- [ ] **Consistency**: Terminology used consistently throughout
- [ ] **Completeness**: All sections in outline are addressed
- [ ] **Clarity**: Technical concepts explained for target audience
- [ ] **Length**: Meets word count requirements
- [ ] **Formatting**: Follows institutional thesis guidelines
- [ ] **Figures/Tables**: Referenced in text before they appear

---

## FINAL NOTES FOR KIMI

1. **Write comprehensively** - Don't rush through sections. Depth over breadth.

2. **Cite as you write** - Every factual claim, statistic, and method description should have a citation.

3. **Use transition sentences** - Connect sections smoothly ("Having established X, the next section examines Y...")

4. **Balance description with analysis** - Don't just describe methods; analyze why they were chosen.

5. **Include critical perspectives** - Acknowledge limitations and counter-arguments.

6. **Write for the target audience** - Assume reader has basic CS/AI knowledge but explain PhishPulse-specific details.

7. **Generate realistic citations** - Use real papers and books. If unsure, use [CITATION NEEDED] markers.

8. **Create descriptive figure captions** - Captions should standalone explain the figure.

9. **Maintain chapter parallelism** - Keep similar structures across chapters for consistency.

10. **Save progress regularly** - Suggest saving each section as separate files for safety.

---

**EXPECTED OUTPUT FORMAT**:
- Plain text or Markdown format
- Clear section headers
- Citations in [Author, Year] format
- Figure/table placeholders clearly marked
- Page breaks between chapters

**BUDGET WORD COUNT**:
- Chapter 1: 5,000 words
- Chapter 2: 8,000 words  
- Chapter 3: 7,000 words
- **Total: ~20,000 words**
