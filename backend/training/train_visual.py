"""
Training script for Model C: Visual Phishing Detector.

Builds perceptual hash database from legitimate brand logos.
"""

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from backend.scanners.visual_detector import VisualPhishingDetector


def train_visual_detector(
    brand_dir: str,
    output_db: str = "models/visual_hashes.db"
):
    """
    Train visual detector by building brand hash database.
    
    Args:
        brand_dir: Directory containing brand logo subdirectories
        output_db: Output SQLite database path
    """
    print(f"Training Visual Phishing Detector...")
    print(f"Brand directory: {brand_dir}")
    print(f"Output database: {output_db}")
    
    # Initialize detector
    detector = VisualPhishingDetector(db_path=output_db)
    
    # Train from directory
    detector.train(brand_dir)
    
    print("\nTraining complete!")
    print(f"Total brand hashes: {sum(len(v) for v in detector.brand_hashes.values())}")


def download_brand_logos(output_dir: str = "data/brand_logos"):
    """
    Download sample brand logos for training.
    
    Note: In production, this would download from official sources.
    For demo purposes, creates placeholder structure.
    """
    print(f"Setting up brand logo directory: {output_dir}")
    
    brands = [
        "paypal", "microsoft", "google", "apple", "amazon",
        "facebook", "netflix", "linkedin", "dropbox", "adobe"
    ]
    
    for brand in brands:
        brand_path = os.path.join(output_dir, brand)
        os.makedirs(brand_path, exist_ok=True)
        print(f"  Created: {brand_path}")
    
    print("\nNote: Add brand logo images (.png, .jpg) to each subdirectory")
    print("Files should be named descriptively (e.g., 'logo.png', 'icon.jpg')")


def main():
    parser = argparse.ArgumentParser(
        description="Train Visual Phishing Detector (ORB + pHash)"
    )
    parser.add_argument(
        "--brand-dir",
        help="Directory containing brand logo subdirectories"
    )
    parser.add_argument(
        "--algorithm",
        choices=['phash', 'dhash', 'whash'],
        default='phash',
        help="Hashing algorithm"
    )
    parser.add_argument(
        "--output",
        default="models/visual_hashes.db",
        help="Output database path"
    )
    parser.add_argument(
        "--download-samples",
        action="store_true",
        help="Download sample brand logos"
    )
    
    args = parser.parse_args()
    
    if args.download_samples:
        download_brand_logos()
        return
    
    if not args.brand_dir:
        parser.error("--brand-dir is required (or use --download-samples)")
    
    # Train
    train_visual_detector(
        brand_dir=args.brand_dir,
        output_db=args.output
    )


if __name__ == "__main__":
    main()
