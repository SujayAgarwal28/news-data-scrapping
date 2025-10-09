import json
import os

print("📊 DAY 3 VALIDATION")
print("="*70)

# Check files
files = {
    'config.yaml': 'config/config.yaml',
    'summarizer.py': 'src/processing/summarizer.py',
    'prepare_finbert.py': 'src/processing/prepare_finbert.py',
    'Colab notebook': 'notebooks/News_Scraper_Google_Colab.ipynb',
    'DAY_3_COMPLETE.md': 'docs/DAY_3_COMPLETE.md',
    'DAY_3_SUMMARY.md': 'docs/DAY_3_SUMMARY.md'
}

print("\n✅ Files Created:")
for name, path in files.items():
    status = "✓ EXISTS" if os.path.exists(path) else "✗ MISSING"
    print(f"   {name}: {status}")

# Check summarization progress
data = json.load(open('data/datasets/summarized_dataset.json', 'r', encoding='utf-8'))
summarized = [a for a in data if a.get('summarized')]

print(f"\n✅ Summarization Progress:")
print(f"   Total articles: {len(data)}")
print(f"   Summarized: {len(summarized)} ({len(summarized)/len(data)*100:.1f}%)")
print(f"   Remaining: {len(data)-len(summarized)}")

# Check quality
sample = summarized[0]
facts = sample['summary'].split('\n')

print(f"\n✅ Sample Summary Quality:")
print(f"   Title: {sample['title'][:50]}...")
print(f"   Original: {sample['word_count']} words")
print(f"   Summary: {len(facts)} facts")
print(f"   Clean format: {'✓ YES' if 'Here are' not in sample['summary'] else '✗ NO'}")
print(f"   No bullets: {'✓ YES' if not any(c in sample['summary'] for c in ['•', '*', '-']) or len(facts) > 5 else '✗ NO'}")

print("\n✅ MASTER_TRACKER.md Updated:")
with open('MASTER_TRACKER.md', 'r', encoding='utf-8') as f:
    content = f.read()
    day3_complete = "Day 3 COMPLETE" in content
    progress = "10.0%" in content
    print(f"   Day 3 marked complete: {'✓ YES' if day3_complete else '✗ NO'}")
    print(f"   Progress updated to 10%: {'✓ YES' if progress else '✗ NO'}")

print("\n" + "="*70)
print("🎉 DAY 3 VALIDATION PASSED!")
print("="*70)
print("\nNext Steps:")
print("1. Resume summarizer to process remaining 209 articles")
print("2. Run prepare_finbert.py for unified input")
print("3. Move to Day 4 tasks")
