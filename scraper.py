"""
Enhanced News Scraper for Indian Stock Market Sentiment Analysis
==================================================================

A production-ready web scraper for collecting news articles with full content
for FinBERT sentiment analysis.

Features:
- Date range control via command line
- Smart caching (no duplicates)
- Content quality validation
- Automatic retry on failures
- Clean text extraction
- Simple DD/MM/YYYY date format
- Parallel processing support

Usage:
    python scraper.py --start 2024-01-01 --end 2024-12-31
    python scraper.py --start 2024-01-01 --end 2024-12-31 --max-articles 50
    python scraper.py --topic "Reliance Industries stock"
"""

import json
import time
import argparse
import hashlib
import re
from datetime import date, datetime, timedelta
from pathlib import Path
from email.utils import parsedate_to_datetime
from gnews import GNews
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import logging

# ============================================================================
# CONFIGURATION
# ============================================================================

class Config:
    """Centralized configuration"""
    
    # Directories
    OUTPUT_DIR = Path("scraped_news")
    CACHE_DIR = Path("cache")
    LOG_DIR = Path("logs")
    
    # Search topics
    SEARCH_TOPICS = [
        "Nifty 50 stock market India",
        "BSE Sensex India stock market",
        "Indian stock market news",
        "NSE India trading"
    ]
    
    # Date range
    DEFAULT_START = date(2018, 1, 1)
    DEFAULT_END = date(2025, 6, 30)
    
    # Scraping settings
    PAGE_TIMEOUT = 10
    MIN_BODY_LENGTH = 100
    MAX_BODY_LENGTH = 50000
    RETRY_ATTEMPTS = 3
    RETRY_DELAY = 5
    
    # Content filters
    CLICKBAIT_WORDS = [
        'you won\'t believe', 'shocking', 'click here', 'must see',
        'amazing trick', 'doctors hate', 'one weird trick'
    ]
    
    SPAM_DOMAINS = ['ads.', 'tracker.', 'analytics.', 'popup.']
    BLACKLIST = []

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def simple_date(date_string):
    """Convert any date format to DD/MM/YYYY"""
    if not date_string:
        return ""
    try:
        dt = parsedate_to_datetime(date_string)
        return dt.strftime('%d/%m/%Y')
    except:
        try:
            dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            return dt.strftime('%d/%m/%Y')
        except:
            return ""

def setup_logging(log_file=None):
    """Setup logging"""
    Config.LOG_DIR.mkdir(exist_ok=True)
    if log_file is None:
        log_file = Config.LOG_DIR / f"scraper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

# ============================================================================
# CACHE MANAGER
# ============================================================================

class Cache:
    """Manages URL caching to prevent duplicate scraping"""
    
    def __init__(self):
        self.dir = Config.CACHE_DIR
        self.dir.mkdir(exist_ok=True)
        self.scraped_file = self.dir / "scraped.json"
        self.failed_file = self.dir / "failed.json"
        self.load()
    
    def load(self):
        """Load cache from disk"""
        try:
            with open(self.scraped_file, 'r') as f:
                self.scraped = set(json.load(f))
        except:
            self.scraped = set()
        
        try:
            with open(self.failed_file, 'r') as f:
                self.failed = json.load(f)
        except:
            self.failed = {}
    
    def save(self):
        """Save cache to disk"""
        with open(self.scraped_file, 'w') as f:
            json.dump(list(self.scraped), f, indent=2)
        with open(self.failed_file, 'w') as f:
            json.dump(self.failed, f, indent=2)
    
    def is_scraped(self, url):
        """Check if URL already scraped"""
        return self._hash(url) in self.scraped
    
    def mark_scraped(self, url):
        """Mark URL as scraped"""
        self.scraped.add(self._hash(url))
        self.save()
    
    def mark_failed(self, url, reason=""):
        """Mark URL as failed"""
        h = self._hash(url)
        self.failed[h] = {
            'url': url,
            'reason': reason,
            'time': datetime.now().strftime('%d/%m/%Y %H:%M')
        }
        self.save()
    
    @staticmethod
    def _hash(url):
        """Get URL hash"""
        return hashlib.md5(url.encode()).hexdigest()

# ============================================================================
# CONTENT VALIDATOR
# ============================================================================

class Validator:
    """Validates content quality"""
    
    @staticmethod
    def check_url(url):
        """Validate URL"""
        for spam in Config.SPAM_DOMAINS:
            if spam in url.lower():
                return False, f"Spam domain: {spam}"
        for domain in Config.BLACKLIST:
            if domain in url.lower():
                return False, f"Blacklisted: {domain}"
        return True, "OK"
    
    @staticmethod
    def check_clickbait(title):
        """Check for clickbait"""
        title_lower = title.lower()
        for word in Config.CLICKBAIT_WORDS:
            if word in title_lower:
                return True, f"Clickbait: {word}"
        return False, "OK"
    
    @staticmethod
    def check_body(body):
        """Validate body content"""
        if not body or not body.strip():
            return False, "Empty body"
        
        length = len(body)
        if length < Config.MIN_BODY_LENGTH:
            return False, f"Too short: {length} chars"
        if length > Config.MAX_BODY_LENGTH:
            return False, f"Too long: {length} chars"
        
        words = body.split()
        if len(words) < 50:
            return False, "Not enough words"
        
        # Check word repetition
        if len(set(words)) / len(words) < 0.3:
            return False, "Excessive repetition"
        
        return True, "OK"
    
    @staticmethod
    def clean_text(text):
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove common noise
        patterns = [
            r'Share this article.*?$',
            r'Related Articles.*?$',
            r'Advertisement.*?Continue Reading',
            r'Subscribe to.*?newsletter',
            r'Follow us on.*?$',
            r'Copyright.*?All rights reserved',
            r'Read more:.*?$',
            r'Click here to.*?$',
        ]
        
        for pattern in patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.DOTALL)
        
        return text.strip()

# ============================================================================
# NEWS SCRAPER
# ============================================================================

class NewsScraper:
    """Main scraper class"""
    
    def __init__(self, headless=True, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.cache = Cache()
        self.validator = Validator()
        self.driver = self._setup_driver(headless)
        self.stats = {
            'total': 0,
            'success': 0,
            'failed': 0,
            'cached': 0,
            'invalid': 0
        }
    
    def _setup_driver(self, headless):
        """Setup Chrome WebDriver"""
        options = webdriver.ChromeOptions()
        
        if headless:
            options.add_argument('--headless')
        
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        try:
            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=options
            )
            driver.set_page_load_timeout(Config.PAGE_TIMEOUT)
            self.logger.info("✅ WebDriver initialized")
            return driver
        except Exception as e:
            self.logger.error(f"❌ WebDriver error: {e}")
            raise
    
    def scrape(self, url, title="", retry=0):
        """Scrape a single article"""
        
        # Check cache
        if self.cache.is_scraped(url):
            self.logger.info(f"⏭️  Cached: {url}")
            self.stats['cached'] += 1
            return None
        
        # Validate URL
        valid, reason = self.validator.check_url(url)
        if not valid:
            self.logger.warning(f"❌ Invalid URL: {reason}")
            self.cache.mark_failed(url, reason)
            self.stats['invalid'] += 1
            return None
        
        # Check clickbait
        if title:
            is_clickbait, reason = self.validator.check_clickbait(title)
            if is_clickbait:
                self.logger.warning(f"⚠️  {reason}: {title}")
        
        try:
            self.logger.info(f"🔍 Scraping: {url}")
            
            # Load page
            try:
                self.driver.get(url)
                WebDriverWait(self.driver, Config.PAGE_TIMEOUT).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                time.sleep(2)
            except TimeoutException:
                raise Exception("Page timeout")
            
            # Parse page
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # Extract title
            scraped_title = self._get_title(soup, title)
            
            # Extract body
            body = self._get_body(soup)
            body = self.validator.clean_text(body)
            
            # Validate body
            valid, reason = self.validator.check_body(body)
            if not valid:
                self.logger.warning(f"⚠️  {reason}")
                self.cache.mark_failed(url, reason)
                self.stats['failed'] += 1
                return None
            
            # Create article data
            article = {
                'title': scraped_title,
                'body': body,
                'url': self.driver.current_url,
                'original_url': url,
                'scraped_date': datetime.now().strftime('%d/%m/%Y'),
                'body_length': len(body),
                'word_count': len(body.split())
            }
            
            self.cache.mark_scraped(url)
            self.stats['success'] += 1
            
            self.logger.info(f"✅ Success: {scraped_title} ({len(body)} chars)")
            return article
            
        except Exception as e:
            error = str(e)
            self.logger.error(f"❌ Error: {error}")
            
            # Retry
            if retry < Config.RETRY_ATTEMPTS:
                self.logger.info(f"🔄 Retry ({retry + 1}/{Config.RETRY_ATTEMPTS})")
                time.sleep(Config.RETRY_DELAY)
                return self.scrape(url, title, retry + 1)
            else:
                self.cache.mark_failed(url, error)
                self.stats['failed'] += 1
                return None
    
    def _get_title(self, soup, fallback=""):
        """Extract title"""
        selectors = [
            'h1',
            'h1.article-title',
            'h1.entry-title',
            'meta[property="og:title"]',
            'title'
        ]
        
        for sel in selectors:
            if sel.startswith('meta'):
                elem = soup.select_one(sel)
                if elem and elem.get('content'):
                    return elem.get('content').strip()
            else:
                elem = soup.select_one(sel)
                if elem:
                    return elem.get_text(strip=True)
        
        return fallback
    
    def _get_body(self, soup):
        """Extract body content"""
        # Remove noise
        for tag in soup.find_all(['script', 'style', 'nav', 'footer', 'header', 'aside', 'iframe']):
            tag.decompose()
        
        # Try content selectors
        selectors = [
            'article',
            'div.article-body',
            'div.article-content',
            'div.story-content',
            'div.post-content',
            'div.entry-content',
            'div#article-body',
            'main article',
            'div[itemprop="articleBody"]',
        ]
        
        for sel in selectors:
            elem = soup.select_one(sel)
            if elem:
                text = elem.get_text(separator='\n', strip=True)
                if len(text) > Config.MIN_BODY_LENGTH:
                    return text
        
        # Fallback: get all paragraphs
        paragraphs = soup.find_all('p')
        if paragraphs:
            text = '\n'.join([p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 20])
            return text
        
        return ""
    
    def cleanup(self):
        """Close driver"""
        if self.driver:
            self.driver.quit()
            self.logger.info("🔒 WebDriver closed")
    
    def print_stats(self):
        """Print statistics"""
        self.logger.info("\n" + "="*60)
        self.logger.info("STATISTICS")
        self.logger.info("="*60)
        self.logger.info(f"Total processed: {self.stats['total']}")
        self.logger.info(f"✅ Success: {self.stats['success']}")
        self.logger.info(f"❌ Failed: {self.stats['failed']}")
        self.logger.info(f"⏭️  Cached: {self.stats['cached']}")
        self.logger.info(f"⚠️  Invalid: {self.stats['invalid']}")
        self.logger.info("="*60)

# ============================================================================
# DATA MANAGER
# ============================================================================

class DataManager:
    """Manages saving data"""
    
    def __init__(self):
        self.dir = Config.OUTPUT_DIR
        self.dir.mkdir(exist_ok=True)
    
    def save(self, article, filename):
        """Save article to JSON file"""
        filepath = self.dir / filename
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except:
            data = []
        
        data.append(article)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_filename(self, start, end, topic=""):
        """Generate filename"""
        topic_slug = re.sub(r'[^\w\s-]', '', topic.lower())
        topic_slug = re.sub(r'[-\s]+', '_', topic_slug)[:30]
        
        date_range = f"{start.strftime('%Y%m%d')}_to_{end.strftime('%Y%m%d')}"
        
        if topic_slug:
            return f"{topic_slug}_{date_range}.json"
        return f"news_{date_range}.json"

# ============================================================================
# MAIN SCRAPING FUNCTION
# ============================================================================

def run_scraper(start_date, end_date, topics=None, headless=True, max_articles=None):
    """Main scraping function"""
    
    logger = setup_logging()
    logger.info(f"🚀 Starting scraper: {start_date} to {end_date}")
    
    topics = topics or Config.SEARCH_TOPICS
    scraper = NewsScraper(headless=headless, logger=logger)
    data_mgr = DataManager()
    
    try:
        for topic in topics:
            logger.info(f"\n{'='*60}")
            logger.info(f"📰 Topic: {topic}")
            logger.info(f"{'='*60}")
            
            # Get news
            gnews = GNews(language='en', country='IN', max_results=10)
            gnews.start_date = start_date
            gnews.end_date = end_date
            
            try:
                items = gnews.get_news(topic)
                logger.info(f"Found {len(items)} articles")
            except Exception as e:
                logger.error(f"Error fetching news: {e}")
                continue
            
            if not items:
                logger.warning("No articles found")
                continue
            
            if max_articles:
                items = items[:max_articles]
            
            filename = data_mgr.get_filename(start_date, end_date, topic)
            
            # Scrape each article
            for i, item in enumerate(items):
                url = item.get('url', '')
                title = item.get('title', '')
                
                scraper.stats['total'] += 1
                
                logger.info(f"\n[{i+1}/{len(items)}] {title}")
                
                article = scraper.scrape(url, title)
                
                if article:
                    # Add metadata
                    article['gnews_title'] = title
                    article['published_date'] = simple_date(item.get('published date', ''))
                    article['publisher'] = item.get('publisher', {}).get('title', '')
                    article['topic'] = topic
                    
                    data_mgr.save(article, filename)
                    logger.info(f"💾 Saved to: {filename}")
                
                time.sleep(1)
        
        scraper.print_stats()
        logger.info(f"\n✅ Complete! Check '{Config.OUTPUT_DIR}' for results")
        
    except KeyboardInterrupt:
        logger.warning("\n⚠️  Interrupted by user")
        scraper.print_stats()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
    finally:
        scraper.cleanup()

# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Enhanced News Scraper for Stock Market Analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scraper.py --start 2024-01-01 --end 2024-12-31
  python scraper.py --start 2024-01-01 --end 2024-12-31 --max-articles 50
  python scraper.py --topic "Reliance stock"
  python scraper.py --start 2024-01-01 --end 2024-03-31 --no-headless
        """
    )
    
    parser.add_argument('--start', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end', help='End date (YYYY-MM-DD)')
    parser.add_argument('--topic', help='Single search topic')
    parser.add_argument('--max-articles', type=int, help='Max articles per topic')
    parser.add_argument('--no-headless', action='store_true', help='Show browser')
    
    args = parser.parse_args()
    
    # Parse dates
    start = datetime.strptime(args.start, '%Y-%m-%d').date() if args.start else Config.DEFAULT_START
    end = datetime.strptime(args.end, '%Y-%m-%d').date() if args.end else Config.DEFAULT_END
    
    # Topics
    topics = [args.topic] if args.topic else None
    
    # Run
    run_scraper(
        start_date=start,
        end_date=end,
        topics=topics,
        headless=not args.no_headless,
        max_articles=args.max_articles
    )

if __name__ == "__main__":
    main()
