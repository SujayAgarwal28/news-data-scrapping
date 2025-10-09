"""
Quick Test - Enhanced Scraper on Real Articles
===============================================

Quick test on 10 real Indian stock market news articles from GNews.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scraping.news_scraper import run_scraper, setup_logging
from datetime import date, timedelta
import json

def quick_test():
    """Quick test with 10 articles"""
    
    print("\n" + "="*70)
    print("QUICK TEST: 10 REAL STOCK MARKET ARTICLES")
    print("="*70 + "\n")
    
    # Setup logging
    logger = setup_logging()
    
    # Test with recent 3-day period
    end_date = date.today()
    start_date = end_date - timedelta(days=3)
    
    print(f"Date Range: {start_date} to {end_date}")
    print(f"Topics: Nifty 50, BSE Sensex, NSE India")
    print(f"Target: 10 articles\n")
    
    # Run scraper
    run_scraper(
        start_date=start_date,
        end_date=end_date,
        topics=["Nifty 50 stock market India"],
        headless=True,
        max_articles=10
    )
    
    print("\n" + "="*70)
    print("QUICK TEST COMPLETE!")
    print("="*70)
    print("\nCheck 'data/raw/news/' folder for scraped articles")
    print("Enhanced features:")
    print("   - Full article body extraction with newspaper3k")
    print("   - Author and publish date metadata")
    print("   - Intelligent fallback to BeautifulSoup")
    print("   - Content quality validation")
    print("\n")

if __name__ == "__main__":
    quick_test()
