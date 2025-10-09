#!/usr/bin/env python3
"""
Prepare Final Dataset for FinBERT
Creates unified 'finbert_input' field from body or summary

Author: StockBus Team
Created: October 9, 2025 (Day 3)
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


def prepare_finbert_dataset(
    input_file: str = "data/datasets/summarized_dataset.json",
    output_file: str = "data/datasets/finbert_input.json"
):
    """
    Create final dataset with unified input field for FinBERT
    
    Logic:
    - If article has 'summary' → use summary
    - Else if 'body' is short enough → use body
    - Adds 'finbert_input' field for consistency
    """
    
    print("\n" + "="*70)
    print("📊 PREPARING FINBERT INPUT DATASET")
    print("="*70)
    
    # Load data
    input_path = project_root / input_file
    with open(input_path, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    print(f"\n📂 Loaded: {len(articles)} articles")
    
    stats = {
        'used_summary': 0,
        'used_body': 0,
        'still_too_long': 0,
        'total_ready': 0
    }
    
    # Process each article
    for article in articles:
        # Determine what to use as FinBERT input
        if article.get('summary'):
            # Use AI-generated summary
            article['finbert_input'] = article['summary']
            article['input_source'] = 'summary'
            stats['used_summary'] += 1
            
        elif article.get('body'):
            # Use original body if short enough
            body = article['body']
            word_count = article.get('word_count', len(body.split()))
            
            if word_count <= 512:
                article['finbert_input'] = body
                article['input_source'] = 'body'
                stats['used_body'] += 1
            else:
                # Still too long (shouldn't happen after summarization)
                article['finbert_input'] = body[:2000]  # Truncate as fallback
                article['input_source'] = 'body_truncated'
                article['warning'] = 'Text truncated - original was too long'
                stats['still_too_long'] += 1
        
        else:
            # No body or summary (edge case)
            article['finbert_input'] = article.get('title', '')
            article['input_source'] = 'title_only'
            article['warning'] = 'No body or summary available'
        
        # Calculate input word count
        article['finbert_input_words'] = len(article['finbert_input'].split())
        
        # Mark as ready
        if article['finbert_input_words'] > 0 and article['finbert_input_words'] <= 512:
            article['finbert_ready'] = True
            stats['total_ready'] += 1
        else:
            article['finbert_ready'] = False
    
    # Save output
    output_path = project_root / output_file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)
    
    # Print statistics
    print("\n" + "="*70)
    print("📊 DATASET PREPARED")
    print("="*70)
    print(f"\n✅ Used AI summaries: {stats['used_summary']}")
    print(f"✅ Used original body: {stats['used_body']}")
    print(f"⚠️ Truncated (still long): {stats['still_too_long']}")
    print(f"\n🎯 Total FinBERT-ready: {stats['total_ready']} / {len(articles)}")
    
    print(f"\n💾 Saved to: {output_path}")
    print(f"📏 File size: {output_path.stat().st_size / 1024 / 1024:.2f} MB")
    
    print("\n" + "="*70)
    print("✅ READY FOR FINBERT!")
    print("="*70)
    print("\nNext steps:")
    print("1. All articles now have 'finbert_input' field")
    print("2. FinBERT will read from this unified field")
    print("3. Move to Day 5: Run FinBERT sentiment analysis")
    print("="*70 + "\n")
    
    return articles


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Prepare unified dataset for FinBERT processing"
    )
    parser.add_argument(
        '--input',
        default='data/datasets/summarized_dataset.json',
        help='Input file (default: summarized_dataset.json)'
    )
    parser.add_argument(
        '--output',
        default='data/datasets/finbert_input.json',
        help='Output file (default: finbert_input.json)'
    )
    
    args = parser.parse_args()
    
    try:
        prepare_finbert_dataset(
            input_file=args.input,
            output_file=args.output
        )
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
