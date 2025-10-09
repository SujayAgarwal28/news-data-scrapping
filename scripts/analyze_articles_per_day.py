"""
Analyze dataset to understand articles per day distribution
"""
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

# Load data
data_file = Path("data/datasets/complete_dataset.json")
with open(data_file, 'r', encoding='utf-8') as f:
    articles = json.load(f)

print("="*70)
print("📊 DATASET ANALYSIS: ARTICLES PER DAY")
print("="*70)

# Parse dates
dates = []
date_errors = 0

for article in articles:
    date_str = article.get('published_date', '')
    if date_str:
        try:
            # Try DD/MM/YYYY format
            dt = datetime.strptime(date_str, '%d/%m/%Y')
            dates.append(dt.date())
        except:
            date_errors += 1
    else:
        date_errors += 1

# Count by date
date_counts = Counter(dates)

print(f"\n📈 Total Articles: {len(articles):,}")
print(f"✅ Articles with valid dates: {len(dates):,}")
print(f"❌ Articles with date errors: {date_errors}")

if date_counts:
    # Statistics
    counts = list(date_counts.values())
    avg = sum(counts) / len(counts)
    max_count = max(counts)
    min_count = min(counts)
    
    print(f"\n📊 Articles Per Day Statistics:")
    print(f"   Average: {avg:.1f} articles/day")
    print(f"   Maximum: {max_count} articles/day")
    print(f"   Minimum: {min_count} articles/day")
    print(f"   Total days: {len(date_counts)} days")
    
    # Distribution
    print(f"\n📈 Distribution:")
    buckets = defaultdict(int)
    for count in counts:
        if count < 5:
            buckets['< 5 articles'] += 1
        elif count < 10:
            buckets['5-10 articles'] += 1
        elif count < 20:
            buckets['10-20 articles'] += 1
        elif count < 30:
            buckets['20-30 articles'] += 1
        else:
            buckets['30+ articles'] += 1
    
    for bucket, day_count in sorted(buckets.items()):
        pct = (day_count / len(date_counts)) * 100
        print(f"   {bucket}: {day_count} days ({pct:.1f}%)")
    
    # Sample recent dates
    print(f"\n📅 Recent Dates (Last 15 days):")
    for date, count in sorted(date_counts.items(), reverse=True)[:15]:
        print(f"   {date}: {count} articles")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    if avg < 15:
        print(f"   ⚠️  Current average ({avg:.1f}/day) is LOW")
        print(f"   📈 Recommended: Aim for 20-30 articles/day")
        print(f"   🎯 Action: Scrape more date ranges or add more topics")
    elif avg < 20:
        print(f"   ✅ Current average ({avg:.1f}/day) is ACCEPTABLE")
        print(f"   📈 Recommended: Aim for 20-30 articles/day for best results")
    elif avg <= 30:
        print(f"   🎯 EXCELLENT! Current average ({avg:.1f}/day) is OPTIMAL")
        print(f"   ✅ This is the sweet spot for sentiment analysis")
    else:
        print(f"   ⚠️  Current average ({avg:.1f}/day) might be HIGH")
        print(f"   💡 Consider: Filtering to top 30 articles/day")
        print(f"   🎯 Reason: Diminishing returns after 30 articles")

print("\n" + "="*70)
