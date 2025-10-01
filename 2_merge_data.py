"""
Script 2: Merge All Scraped JSON Files
=======================================
Combines all JSON files from scraped_news/ into a single dataset.
Removes duplicates and analyzes data quality.

Usage:
    python 2_merge_data.py
"""

import json
import glob
from pathlib import Path
from collections import Counter

def load_all():
    """Load all articles from JSON files"""
    news_dir = Path("scraped_news")
    
    if not news_dir.exists():
        print("❌ Directory 'scraped_news' not found!")
        return []
    
    all_articles = []
    files = list(news_dir.glob("*.json"))
    
    print(f"📂 Found {len(files)} JSON files\n")
    
    for json_file in files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                articles = json.load(f)
                all_articles.extend(articles)
                print(f"✅ {json_file.name}: {len(articles)} articles")
        except Exception as e:
            print(f"❌ Error loading {json_file.name}: {e}")
    
    print(f"\n📊 Total: {len(all_articles)} articles")
    return all_articles

def remove_duplicates(articles):
    """Remove duplicate articles by URL"""
    seen = set()
    unique = []
    dups = 0
    
    for art in articles:
        url = art.get('url', '')
        if url and url not in seen:
            seen.add(url)
            unique.append(art)
        else:
            dups += 1
    
    if dups > 0:
        print(f"🔍 Removed {dups} duplicates")
    
    return unique

def analyze(articles):
    """Analyze dataset"""
    print("\n" + "="*70)
    print("DATASET ANALYSIS")
    print("="*70)
    
    print(f"\n📈 Total Articles: {len(articles)}")
    
    # Word count stats
    word_counts = [art.get('word_count', 0) for art in articles]
    if word_counts:
        print(f"\n📝 Word Count:")
        print(f"   Min: {min(word_counts)}")
        print(f"   Max: {max(word_counts)}")
        print(f"   Average: {sum(word_counts) // len(word_counts)}")
    
    # Length categories for FinBERT
    very_short = sum(1 for wc in word_counts if wc < 50)
    short = sum(1 for wc in word_counts if 50 <= wc < 200)
    medium = sum(1 for wc in word_counts if 200 <= wc <= 512)
    long = sum(1 for wc in word_counts if 512 < wc <= 1000)
    very_long = sum(1 for wc in word_counts if wc > 1000)
    
    print(f"\n📊 Length Distribution (for FinBERT):")
    print(f"   Very Short (<50): {very_short} ({very_short/len(articles)*100:.1f}%)")
    print(f"   Short (50-200): {short} ({short/len(articles)*100:.1f}%)")
    print(f"   Medium (200-512): {medium} ({medium/len(articles)*100:.1f}%) ✅ Ideal")
    print(f"   Long (512-1000): {long} ({long/len(articles)*100:.1f}%) ⚠️ Summarize")
    print(f"   Very Long (>1000): {very_long} ({very_long/len(articles)*100:.1f}%) ⚠️ Summarize")
    
    # Publishers
    publishers = [art.get('publisher', 'Unknown') for art in articles if art.get('publisher')]
    if publishers:
        top = Counter(publishers).most_common(10)
        print(f"\n📰 Top 10 Publishers:")
        for pub, count in top:
            print(f"   {pub}: {count}")
    
    # Topics
    topics = [art.get('topic', 'Unknown') for art in articles if art.get('topic')]
    if topics:
        counts = Counter(topics)
        print(f"\n🔍 Articles per Topic:")
        for topic, count in counts.items():
            print(f"   {topic}: {count}")
    
    # Date range
    dates = [art.get('published_date', '') for art in articles if art.get('published_date')]
    if dates:
        dates = [d for d in dates if d]  # Remove empty
        print(f"\n📅 Date Range:")
        print(f"   Earliest: {min(dates)}")
        print(f"   Latest: {max(dates)}")
    
    print("\n" + "="*70)

def save_merged(articles, filename="complete_dataset.json"):
    """Save merged dataset"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    
    size_mb = Path(filename).stat().st_size / (1024 * 1024)
    print(f"\n💾 Saved: {filename}")
    print(f"   Size: {size_mb:.2f} MB")

def create_finbert_ready(articles, filename="finbert_ready.json"):
    """Create FinBERT-ready dataset with processing flags"""
    for art in articles:
        wc = art.get('word_count', 0)
        
        if 200 <= wc <= 512:
            art['processing'] = 'ready'
            art['finbert_ready'] = True
        elif 50 <= wc < 200:
            art['processing'] = 'use_as_is'
            art['finbert_ready'] = True
        elif wc > 512:
            art['processing'] = 'needs_t5_summary'
            art['finbert_ready'] = False
        else:
            art['processing'] = 'too_short'
            art['finbert_ready'] = False
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    
    ready = sum(1 for a in articles if a['finbert_ready'])
    needs_summary = sum(1 for a in articles if a['processing'] == 'needs_t5_summary')
    too_short = sum(1 for a in articles if a['processing'] == 'too_short')
    
    print(f"\n📋 FinBERT Dataset: {filename}")
    print(f"   ✅ Ready: {ready}")
    print(f"   ⚠️ Need summary: {needs_summary}")
    print(f"   ❌ Too short: {too_short}")

def main():
    print("="*70)
    print("MERGE SCRAPED DATA")
    print("="*70)
    
    # Load
    print("\n🔄 Loading articles...")
    articles = load_all()
    
    if not articles:
        print("❌ No articles found!")
        return
    
    # Remove duplicates
    print("\n🔍 Removing duplicates...")
    articles = remove_duplicates(articles)
    
    # Analyze
    analyze(articles)
    
    # Save
    print("\n💾 Saving datasets...")
    save_merged(articles, "complete_dataset.json")
    create_finbert_ready(articles, "finbert_ready.json")
    
    print("\n" + "="*70)
    print("✅ COMPLETE!")
    print("="*70)
    print("\nFiles created:")
    print("1. complete_dataset.json - All articles merged")
    print("2. finbert_ready.json - Tagged for FinBERT processing")
    print("\nNext steps:")
    print("- Use finbert_ready.json for your ML pipeline")
    print("- Articles with 'needs_t5_summary' should be summarized first")
    print("="*70)

if __name__ == "__main__":
    main()
