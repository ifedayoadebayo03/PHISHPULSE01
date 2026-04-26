"""
Training script for Model B: Email Forensic Analyzer (Naive Bayes).

Supervised training with incremental learning support.
"""

import argparse
import csv
import json
from typing import List, Tuple

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from backend.scanners.email_forensics import EmailForensicAnalyzer


def load_enron_emails(filepath: str, max_emails: int = 50000) -> List[str]:
    """Load emails from Enron dataset format."""
    emails = []
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        # Simple split by "From:" which starts most emails
        messages = content.split('\nFrom:')
        for msg in messages[:max_emails]:
            if msg.strip():
                emails.append(msg.strip())
    return emails


def load_emails_from_csv(filepath: str, text_column: str = 'text', label_column: str = 'label') -> Tuple[List[str], List[int]]:
    """Load emails and labels from CSV."""
    emails = []
    labels = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if text_column in row:
                emails.append(row[text_column])
                labels.append(int(row.get(label_column, 0)))
    
    return emails, labels


def load_emails_from_jsonl(filepath: str) -> Tuple[List[str], List[int]]:
    """Load emails from JSONL format."""
    emails = []
    labels = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            emails.append(data.get('text', data.get('body', '')))
            labels.append(int(data.get('label', 0)))
    
    return emails, labels


def train_email_model(
    benign_emails: List[str],
    phishing_emails: List[str],
    batch_size: int = 500
):
    """
    Train Email Forensic Analyzer with incremental learning.
    
    Uses partial_fit for memory efficiency on 7.4GB RAM.
    """
    print(f"Training Email Forensic Analyzer...")
    print(f"Benign emails: {len(benign_emails)}")
    print(f"Phishing emails: {len(phishing_emails)}")
    
    # Initialize analyzer
    analyzer = EmailForensicAnalyzer()
    
    # Combine and create labels
    all_emails = benign_emails + phishing_emails
    all_labels = [0] * len(benign_emails) + [1] * len(phishing_emails)
    
    print(f"\nTotal training samples: {len(all_emails)}")
    print(f"Batch size: {batch_size}")
    
    # Train in batches with partial_fit
    from sklearn.feature_extraction.text import HashingVectorizer
    
    vectorizer = HashingVectorizer(
        n_features=1024,
        alternate_sign=False
    )
    
    # Initialize model
    from sklearn.naive_bayes import MultinomialNB
    model = MultinomialNB()
    
    print("\nTraining...")
    
    # Process in batches
    for i in range(0, len(all_emails), batch_size):
        batch_emails = all_emails[i:i+batch_size]
        batch_labels = all_labels[i:i+batch_size]
        
        print(f"  Batch {i//batch_size + 1}/{(len(all_emails) + batch_size - 1)//batch_size}")
        
        # Vectorize batch
        X_batch = vectorizer.transform(batch_emails)
        
        # Partial fit
        if i == 0:
            model.partial_fit(X_batch, batch_labels, classes=[0, 1])
        else:
            model.partial_fit(X_batch, batch_labels)
    
    # Save model
    analyzer.model = model
    analyzer.vectorizer = vectorizer
    analyzer.is_fitted = True
    analyzer._save_model()
    
    print("\nTraining complete!")
    
    # Validation metrics
    print("\nValidation metrics:")
    from sklearn.metrics import classification_report
    
    X_test = vectorizer.transform(all_emails)
    predictions = model.predict(X_test)
    
    print(classification_report(all_labels, predictions, target_names=['Benign', 'Phishing']))


def main():
    parser = argparse.ArgumentParser(
        description="Train Email Forensic Analyzer (Naive Bayes)"
    )
    parser.add_argument(
        "--benign",
        required=True,
        help="Path to benign emails (CSV, TXT, or JSONL)"
    )
    parser.add_argument(
        "--phishing",
        required=True,
        help="Path to phishing emails (CSV, TXT, or JSONL)"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=500,
        help="Batch size for memory efficiency (default: 500)"
    )
    parser.add_argument(
        "--format",
        choices=['csv', 'jsonl', 'txt'],
        default='csv',
        help="Input file format"
    )
    
    args = parser.parse_args()
    
    # Load benign emails
    if args.format == 'csv':
        benign_emails, _ = load_emails_from_csv(args.benign, label_column=None)
        phishing_emails, _ = load_emails_from_csv(args.phishing, label_column=None)
    elif args.format == 'jsonl':
        benign_emails, _ = load_emails_from_jsonl(args.benign)
        phishing_emails, _ = load_emails_from_jsonl(args.phishing)
    else:
        with open(args.benign, 'r') as f:
            benign_emails = f.read().split('\n\n')
        with open(args.phishing, 'r') as f:
            phishing_emails = f.read().split('\n\n')
    
    # Train
    train_email_model(
        benign_emails=benign_emails,
        phishing_emails=phishing_emails,
        batch_size=args.batch_size
    )


if __name__ == "__main__":
    main()
