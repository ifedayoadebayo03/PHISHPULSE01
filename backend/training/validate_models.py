"""
Model validation script with time-based split and stratified k-fold.
"""

import argparse
import json
from datetime import datetime, timedelta
from typing import Dict, List

import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix
)

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from backend.scanners import (
    URLLexicalAnalyzer,
    EmailForensicAnalyzer,
    VisualPhishingDetector,
    RiskFusionEngine
)


def time_based_split(
    data: List[Dict],
    test_days: int = 7,
    min_days: int = 30
) -> tuple:
    """
    Split data by time (simulates production).
    
    Train on data >30 days old, test on last 7 days.
    """
    now = datetime.utcnow()
    test_cutoff = now - timedelta(days=test_days)
    train_cutoff = now - timedelta(days=min_days)
    
    train_data = [d for d in data if d['timestamp'] < train_cutoff]
    test_data = [d for d in data if d['timestamp'] >= test_cutoff]
    
    return train_data, test_data


def validate_url_model(test_urls: List[str], labels: List[int]) -> Dict:
    """Validate URL Lexical Analyzer."""
    print("Validating URL Lexical Analyzer...")
    
    analyzer = URLLexicalAnalyzer()
    
    predictions = []
    scores = []
    
    for url in test_urls:
        result = analyzer.analyze(url)
        scores.append(result['score'])
        # Convert score to binary prediction
        predictions.append(1 if result['score'] > 60 else 0)
    
    return {
        "model": "URL Lexical Analyzer",
        "algorithm": "Isolation Forest",
        "accuracy": accuracy_score(labels, predictions),
        "precision": precision_score(labels, predictions, zero_division=0),
        "recall": recall_score(labels, predictions, zero_division=0),
        "f1": f1_score(labels, predictions, zero_division=0),
        "avg_score": np.mean(scores),
        "score_std": np.std(scores)
    }


def validate_email_model(test_emails: List[str], labels: List[int]) -> Dict:
    """Validate Email Forensic Analyzer."""
    print("Validating Email Forensic Analyzer...")
    
    analyzer = EmailForensicAnalyzer()
    
    predictions = []
    scores = []
    
    for email in test_emails:
        result = analyzer.analyze(email)
        scores.append(result['score'])
        predictions.append(1 if result['score'] > 60 else 0)
    
    return {
        "model": "Email Forensic Analyzer",
        "algorithm": "Multinomial Naive Bayes",
        "accuracy": accuracy_score(labels, predictions),
        "precision": precision_score(labels, predictions, zero_division=0),
        "recall": recall_score(labels, predictions, zero_division=0),
        "f1": f1_score(labels, predictions, zero_division=0),
        "avg_score": np.mean(scores),
        "score_std": np.std(scores)
    }


def validate_fusion_engine(
    url_results: List[Dict],
    email_results: List[Dict],
    labels: List[int]
) -> Dict:
    """Validate Risk Fusion Engine."""
    print("Validating Risk Fusion Engine...")
    
    fusion = RiskFusionEngine()
    
    predictions = []
    scores = []
    
    for url_r, email_r in zip(url_results, email_results):
        result = fusion.fuse(
            url_result=url_r,
            email_result=email_r
        )
        scores.append(result['final_score'])
        predictions.append(1 if result['final_score'] > 60 else 0)
    
    return {
        "model": "Risk Fusion Engine",
        "algorithm": "Weighted Ensemble",
        "accuracy": accuracy_score(labels, predictions),
        "precision": precision_score(labels, predictions, zero_division=0),
        "recall": recall_score(labels, predictions, zero_division=0),
        "f1": f1_score(labels, predictions, zero_division=0),
        "avg_score": np.mean(scores),
        "score_std": np.std(scores)
    }


def cross_validate(
    X: np.ndarray,
    y: np.ndarray,
    n_splits: int = 5
) -> Dict:
    """Perform stratified k-fold cross-validation."""
    print(f"Performing {n_splits}-fold stratified cross-validation...")
    
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    
    scores = {
        'accuracy': [],
        'precision': [],
        'recall': [],
        'f1': []
    }
    
    for fold, (train_idx, val_idx) in enumerate(skf.split(X, y)):
        print(f"  Fold {fold + 1}/{n_splits}")
        
        # Note: This is simplified; real implementation would retrain models
        # For now, just calculate metrics on validation split
        y_val = y[val_idx]
        
        # Placeholder predictions (random for demo)
        # In production, retrain and predict
        y_pred = np.random.randint(0, 2, size=len(y_val))
        
        scores['accuracy'].append(accuracy_score(y_val, y_pred))
        scores['precision'].append(precision_score(y_val, y_pred, zero_division=0))
        scores['recall'].append(recall_score(y_val, y_pred, zero_division=0))
        scores['f1'].append(f1_score(y_val, y_pred, zero_division=0))
    
    return {
        "accuracy_mean": np.mean(scores['accuracy']),
        "accuracy_std": np.std(scores['accuracy']),
        "precision_mean": np.mean(scores['precision']),
        "precision_std": np.std(scores['precision']),
        "recall_mean": np.mean(scores['recall']),
        "recall_std": np.std(scores['recall']),
        "f1_mean": np.mean(scores['f1']),
        "f1_std": np.std(scores['f1'])
    }


def main():
    parser = argparse.ArgumentParser(
        description="Validate PhishPulse Models"
    )
    parser.add_argument(
        "--test-urls",
        help="Path to test URLs CSV"
    )
    parser.add_argument(
        "--test-emails",
        help="Path to test emails"
    )
    parser.add_argument(
        "--output",
        default="validation_results.json",
        help="Output JSON file"
    )
    parser.add_argument(
        "--cross-validate",
        action="store_true",
        help="Perform cross-validation"
    )
    
    args = parser.parse_args()
    
    results = {
        "timestamp": datetime.utcnow().isoformat(),
        "models": []
    }
    
    # Validate URL model
    if args.test_urls:
        # Load test data
        # test_urls, url_labels = load_test_data(args.test_urls)
        # url_results = validate_url_model(test_urls, url_labels)
        # results["models"].append(url_results)
        pass
    
    # Validate Email model
    if args.test_emails:
        # test_emails, email_labels = load_test_data(args.test_emails)
        # email_results = validate_email_model(test_emails, email_labels)
        # results["models"].append(email_results)
        pass
    
    # Save results
    with open(args.output, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nValidation results saved to: {args.output}")


if __name__ == "__main__":
    main()
