"""
Training script for Model A: URL Lexical Analyzer (Isolation Forest).

Unsupervised training on benign URLs only - no malicious examples required.
"""

import argparse
import csv
import gc
from typing import List

import numpy as np
from sklearn.ensemble import IsolationForest

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from backend.scanners.url_lexical import URLLexicalAnalyzer


def load_urls_from_csv(filepath: str) -> List[str]:
    """Load URLs from CSV file."""
    urls = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                url = row[0].strip()
                if url.startswith('http'):
                    urls.append(url)
    return urls


def load_urls_from_txt(filepath: str) -> List[str]:
    """Load URLs from text file (one per line)."""
    urls = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            url = line.strip()
            if url.startswith('http'):
                urls.append(url)
    return urls


def train_in_batches(
    urls: List[str],
    batch_size: int = 1000,
    contamination: float = 0.1,
    output_path: str = "models/url_isolation_forest.pkl.gz"
):
    """
    Train Isolation Forest with batch processing for memory efficiency.
    
    Due to 7.4GB RAM constraint, we process in batches with warm_start.
    """
    print(f"Training on {len(urls)} benign URLs...")
    print(f"Batch size: {batch_size}")
    print(f"Contamination: {contamination}")
    
    # Initialize analyzer
    analyzer = URLLexicalAnalyzer()
    
    # Extract features for all URLs
    print("Extracting features...")
    X = np.array([analyzer._extract_features(url) for url in urls])
    
    print(f"Feature matrix shape: {X.shape}")
    
    # Initialize model with warm_start
    model = IsolationForest(
        contamination=contamination,
        warm_start=True,
        n_estimators=50,
        max_samples=0.8,
        random_state=42,
        n_jobs=-1
    )
    
    # Initial fit on first batch
    print("Initial training...")
    initial_batch = X[:min(batch_size, len(X))]
    model.fit(initial_batch)
    
    # Incremental training on remaining batches
    for i in range(batch_size, len(X), batch_size):
        batch = X[i:i+batch_size]
        print(f"Processing batch {i//batch_size + 1}/{(len(X) + batch_size - 1)//batch_size}...")
        
        # Increment estimators
        model.n_estimators += 10
        model.fit(batch)
        
        # Force garbage collection
        gc.collect()
    
    # Save model
    analyzer.model = model
    analyzer.is_fitted = True
    analyzer._save_model()
    
    print(f"\nTraining complete!")
    print(f"Model saved to: {output_path}")
    
    # Calculate outlier scores
    outlier_scores = model.decision_function(X)
    print(f"\nOutlier score statistics:")
    print(f"  Mean: {outlier_scores.mean():.4f}")
    print(f"  Std: {outlier_scores.std():.4f}")
    print(f"  Min: {outlier_scores.min():.4f}")
    print(f"  Max: {outlier_scores.max():.4f}")


def main():
    parser = argparse.ArgumentParser(
        description="Train URL Lexical Analyzer (Isolation Forest)"
    )
    parser.add_argument(
        "--benign-data",
        required=True,
        help="Path to benign URLs CSV/TXT file"
    )
    parser.add_argument(
        "--contamination",
        type=float,
        default=0.1,
        help="Contamination parameter (default: 0.1)"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=1000,
        help="Batch size for memory efficiency (default: 1000)"
    )
    parser.add_argument(
        "--output",
        default="models/url_isolation_forest.pkl.gz",
        help="Output model path"
    )
    
    args = parser.parse_args()
    
    # Load URLs
    if args.benign_data.endswith('.csv'):
        urls = load_urls_from_csv(args.benign_data)
    else:
        urls = load_urls_from_txt(args.benign_data)
    
    print(f"Loaded {len(urls)} URLs")
    
    # Train
    train_in_batches(
        urls=urls,
        batch_size=args.batch_size,
        contamination=args.contamination,
        output_path=args.output
    )


if __name__ == "__main__":
    main()
