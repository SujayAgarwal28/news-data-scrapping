import json

# Load and check summarized dataset
with open('data/datasets/summarized_dataset.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

summarized = [a for a in data if a.get('summarized')]

print(f"✅ Summarized: {len(summarized)}/{len(data)} articles ({len(summarized)/len(data)*100:.1f}%)")
print(f"\n📊 Sample Summary:")
print("="*70)
if summarized:
    sample = summarized[5]
    print(f"Title: {sample['title'][:60]}...")
    print(f"Original: {sample['word_count']} words")
    print(f"\nSummary:\n{sample['summary'][:400]}")
    print("="*70)
