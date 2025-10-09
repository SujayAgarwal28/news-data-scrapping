"""
Script 3: Quick Test Run
=========================
Test the scraper with a small sample (last 7 days, 5 articles).

Usage:
    python 3_test.py
"""

from datetime import date, timedelta
from scraper import run_scraper

print("="*70)
print("QUICK TEST RUN")
print("="*70)

end = date.today()
start = end - timedelta(days=7)

print(f"Date range: {start} to {end}")
print(f"Articles: 5 per topic (for testing)")
print("="*70)
print()

run_scraper(
    start_date=start,
    end_date=end,
    topics=["Nifty 50 India"],
    headless=True,
    max_articles=5
)

print("\n" + "="*70)
print("✅ TEST COMPLETE!")
print("="*70)
print("\nCheck these directories:")
print("- scraped_news/ - Output JSON files")
print("- logs/ - Detailed logs")
print("- cache/ - Cached URLs")
print("\nIf successful, run the full scraper:")
print("python scraper.py --start 2018-01-01 --end 2025-06-30")
print("="*70)
