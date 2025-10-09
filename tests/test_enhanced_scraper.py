"""
Test Enhanced News Scraper with newspaper3k
============================================

Test the enhanced scraper on real Indian stock market news articles.
Validates body extraction, metadata, and data quality.

Usage:
    python tests/test_enhanced_scraper.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scraping.news_scraper import NewsScraper, setup_logging
import json
from datetime import datetime

# Test URLs from major Indian financial news sources
TEST_URLS = [
    # Economic Times
    "https://economictimes.indiatimes.com/markets/stocks/news",
    
    # Moneycontrol  
    "https://www.moneycontrol.com/news/business/markets/",
    
    # Business Standard
    "https://www.business-standard.com/markets",
]

def test_scraper():
    """Test the enhanced scraper"""
    
    print("\n" + "="*70)
    print("🧪 TESTING ENHANCED NEWS SCRAPER WITH NEWSPAPER3K")
    print("="*70 + "\n")
    
    # Setup logging
    logger = setup_logging()
    
    # Initialize scraper
    print("🚀 Initializing scraper...")
    scraper = NewsScraper(headless=True, logger=logger)
    
    results = []
    
    try:
        # Test on sample URLs
        print(f"\n📰 Testing on {len(TEST_URLS)} sample news pages...\n")
        
        for i, url in enumerate(TEST_URLS, 1):
            print(f"\n{'='*70}")
            print(f"Test {i}/{len(TEST_URLS)}: {url}")
            print(f"{'='*70}")
            
            try:
                article = scraper.scrape(url, title=f"Test Article {i}")
                
                if article:
                    print(f"\n✅ SUCCESS!")
                    print(f"   Title: {article['title'][:80]}...")
                    print(f"   Body Length: {article['body_length']:,} characters")
                    print(f"   Word Count: {article['word_count']:,} words")
                    print(f"   Extraction Method: {article['extraction_method']}")
                    print(f"   Published: {article.get('published_date', 'N/A')}")
                    print(f"   Authors: {', '.join(article.get('authors', [])) or 'N/A'}")
                    
                    # Show first 200 chars of body
                    print(f"\n   📄 Body Preview:")
                    print(f"   {article['body'][:200]}...")
                    
                    results.append({
                        'url': url,
                        'status': 'success',
                        'body_length': article['body_length'],
                        'method': article['extraction_method']
                    })
                else:
                    print(f"\n⚠️  FAILED - No article extracted")
                    results.append({
                        'url': url,
                        'status': 'failed',
                        'body_length': 0,
                        'method': 'none'
                    })
                    
            except Exception as e:
                print(f"\n❌ ERROR: {e}")
                results.append({
                    'url': url,
                    'status': 'error',
                    'error': str(e)
                })
        
        # Print summary
        print("\n" + "="*70)
        print("📊 TEST SUMMARY")
        print("="*70)
        
        scraper.print_stats()
        
        # Method breakdown
        newspaper3k_count = sum(1 for r in results if r.get('method') == 'newspaper3k')
        beautifulsoup_count = sum(1 for r in results if r.get('method') == 'beautifulsoup')
        
        print(f"\n🔧 EXTRACTION METHOD BREAKDOWN:")
        print(f"   newspaper3k: {newspaper3k_count}")
        print(f"   beautifulsoup: {beautifulsoup_count}")
        
        # Body length analysis
        successful = [r for r in results if r.get('status') == 'success']
        if successful:
            avg_length = sum(r['body_length'] for r in successful) / len(successful)
            print(f"\n📏 AVERAGE BODY LENGTH:")
            print(f"   {avg_length:,.0f} characters")
        
        # Save test results
        output_file = Path("tests") / f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'total_tests': len(TEST_URLS),
                'results': results,
                'stats': scraper.stats
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Results saved to: {output_file}")
        
        print("\n" + "="*70)
        print("✅ TEST COMPLETE!")
        print("="*70 + "\n")
        
    finally:
        scraper.cleanup()

if __name__ == "__main__":
    test_scraper()
