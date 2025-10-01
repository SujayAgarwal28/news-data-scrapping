# 📰 News Scraper for Indian Stock Market

A production-ready web scraper for collecting news articles with full text content for sentiment analysis using FinBERT.

## 🎯 What This Does

Scrapes Indian stock market news from Google News with:
- Full article text (cleaned and validated)
- Simple date format (DD/MM/YYYY)
- Smart caching (never scrapes the same URL twice)
- Quality filters (removes clickbait, spam, short articles)
- Parallel processing support

## 📦 Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## 🚀 Quick Start

### 1️⃣ Test Run (Recommended First)

```bash
python 3_test.py
```

This scrapes last 7 days with 5 articles to verify everything works.

### 2️⃣ Scrape Specific Date Range

```bash
# Simple usage
python scraper.py --start 2024-01-01 --end 2024-12-31

# Limit articles
python scraper.py --start 2024-01-01 --end 2024-12-31 --max-articles 50

# Specific topic
python scraper.py --start 2024-01-01 --end 2024-12-31 --topic "Reliance stock"
```

### 3️⃣ Parallel Scraping (For Large Date Ranges)

For scraping 2018-2025 (7 years), use parallel jobs:

```bash
# Generate 8 parallel jobs
python 1_generate_jobs.py --start 2018-01-01 --end 2025-06-30 --splits 8

# Run the batch file (Windows)
run_all.bat
```

This opens 8 terminal windows, each scraping ~10 months. Much faster!

### 4️⃣ Merge Results (If Using Multiple Computers)

After scraping on multiple machines, collect all JSON files in `scraped_news/` folder, then:

```bash
python 2_merge_data.py
```

This creates:
- `complete_dataset.json` - All articles combined
- `finbert_ready.json` - Tagged for ML processing

## 📁 File Structure

```
scraper.py              # Main scraper (use this)
1_generate_jobs.py      # Generate parallel jobs
2_merge_data.py         # Merge all scraped data
3_test.py               # Quick test run

requirements.txt        # Dependencies

scraped_news/           # Output JSON files (created automatically)
cache/                  # Prevents duplicate scraping
logs/                   # Detailed logs
```

## 📊 Output Format

Each JSON file contains articles in this format:

```json
[
  {
    "title": "Nifty 50 reaches new high...",
    "body": "Full article text here...",
    "url": "https://example.com/article",
    "published_date": "01/10/2024",
    "scraped_date": "01/10/2024",
    "word_count": 412,
    "body_length": 2543,
    "publisher": "Economic Times",
    "topic": "Nifty 50 stock market India"
  }
]
```

**Simple dates**: `DD/MM/YYYY` format - easy to parse for ML!

## 🔧 Advanced Usage

### Parallel Scraping on Multiple Computers

**Computer 1:**
```bash
python scraper.py --start 2018-01-01 --end 2019-12-31
```

**Computer 2:**
```bash
python scraper.py --start 2020-01-01 --end 2021-12-31
```

**Computer 3:**
```bash
python scraper.py --start 2022-01-01 --end 2023-12-31
```

**Computer 4:**
```bash
python scraper.py --start 2024-01-01 --end 2025-06-30
```

Then collect all `scraped_news/*.json` files and run `2_merge_data.py`.

### Custom Topics

Edit `scraper.py`, find `Config.SEARCH_TOPICS` and add your topics:

```python
SEARCH_TOPICS = [
    "Nifty 50 stock market India",
    "BSE Sensex India",
    "Reliance Industries stock",  # Add your topics here
    "TCS stock news",
]
```

## 💡 For Your ML Project

### Data Quality

The scraper ensures:
- ✅ Minimum 100 characters
- ✅ Maximum 50,000 characters
- ✅ At least 50 words
- ✅ No excessive repetition
- ✅ Cleaned (ads/navigation removed)

### Using with FinBERT

```python
import json

# Load data
with open('finbert_ready.json') as f:
    articles = json.load(f)

# Filter ready articles
ready = [a for a in articles if a['finbert_ready']]

# Articles needing T5 summarization first
needs_summary = [a for a in articles if a['processing'] == 'needs_t5_summary']
```

## ⚙️ Configuration

Edit `Config` class in `scraper.py`:

```python
class Config:
    # Directories
    OUTPUT_DIR = Path("scraped_news")
    CACHE_DIR = Path("cache")
    LOG_DIR = Path("logs")
    
    # Topics
    SEARCH_TOPICS = [...]
    
    # Date range
    DEFAULT_START = date(2018, 1, 1)
    DEFAULT_END = date(2025, 6, 30)
    
    # Quality filters
    MIN_BODY_LENGTH = 100
    MAX_BODY_LENGTH = 50000
```

## 🐛 Troubleshooting

### No articles found

- Try shorter date ranges
- Check internet connection
- GNews has limits on old articles

### Chrome/WebDriver errors

- Make sure Chrome browser is installed
- Update Chrome to latest version
- The script auto-downloads ChromeDriver

### Too many timeouts

- Normal! The scraper retries automatically
- Failed URLs are saved in `cache/failed.json`
- You can review and manually handle if needed

### Clear cache

```bash
# Windows
rmdir /s cache
mkdir cache

# Or just delete the cache folder and restart
```

## 📈 Expected Results

For 2018-2025 dataset:
- **Topics**: 4 default topics
- **Articles**: 1,000-3,000 (varies by date)
- **Success rate**: ~70-80%
- **Time**: 
  - Single run: 6-12 hours
  - 8 parallel jobs: 1-2 hours

## 🎓 Workflow Summary

```
1. Test: python 3_test.py
         ↓
2. Generate jobs: python 1_generate_jobs.py --start 2018-01-01 --end 2025-06-30 --splits 8
         ↓
3. Run jobs: run_all.bat (or distribute to multiple computers)
         ↓
4. Merge data: python 2_merge_data.py
         ↓
5. Use finbert_ready.json for your ML project!
```

## 📝 Notes

- **Dates**: All dates are DD/MM/YYYY for easy parsing
- **Cache**: Prevents duplicate scraping even across multiple runs
- **Quality**: Articles are validated and cleaned automatically
- **Resume**: If interrupted, just run again - cache handles duplicates

## 🚦 Quick Commands

```bash
# Test
python 3_test.py

# Full scrape
python scraper.py --start 2018-01-01 --end 2025-06-30

# Parallel (8 jobs)
python 1_generate_jobs.py --start 2018-01-01 --end 2025-06-30 --splits 8
run_all.bat

# Merge results
python 2_merge_data.py
```

---

**Good luck with your sentiment analysis project! 🚀📈**

If you have issues, check the `logs/` folder for detailed error messages.
